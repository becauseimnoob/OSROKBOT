import json
import openai
import os
from dotenv import load_dotenv
from Actions.manual_click_action import ManualClickAction
import time
from termcolor import colored
import os

class ChatGPTAction:
    def __init__(self,midterm=False, prefix= "", filepath="string.txt"):
        
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_KEY')
        self.message = ""
        self.prefix = prefix
        self.filepath = filepath
        self.midterm = midterm
        self.messages = [{"role": "system", "content": "You are a quizz assistant in the game Rise of Kingdoms."}]
        self.functions = [
        {
            "name": "return_option_based_on_prompt",
            "description": "Returns the response to the question in the prompt, ignoring the answer options, returns the chosen answer option (A, B, C or D) based on the prompt, and returns the percentage of how certain it is of that answer option.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answerComplete": {
                        "type": "string",
                        "description": "Quick response to the question in the prompt, step by step chain of thought, ignoring the answer options.",
                    },
                    "answer": {
                        "type": "string",
                        "enum": ["A", "B", "C", "D"],
                        "description": "The chosen answer option to the question in the prompt.",
                    },
                    
                    "certainty": {
                        "type": "integer",
                        "description": "The certainty percentage of the chosen answer option to the question in the prompt.",
                    },
                },
                "required": ["answer,certainty,answerComplete"],
            },
        }
        ]

    def find_option(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith((' A:', ' B:', ' C:', ' D:')):
                return line.strip()  # Removing trailing new line
                    
    def execute(self):
        os.system('cls')
        with open(self.filepath, 'r') as file:
            self.message = file.read()
            print(f"User: {self.message}")
        #concatenate prefix and message
        self.message = self.prefix + self.message
        
        self.messages.append({"role": "user", "content": (self.message)},)
        chat = openai.ChatCompletion.create(
            model="gpt-4-0613",
            temperature=0.1,
            messages=self.messages,
            functions=self.functions,
            function_call={"name": "return_option_based_on_prompt"}
        )

        response_message = chat.choices[0].message
        

        if response_message.get("function_call"):
            function_arguments = json.loads(response_message["function_call"]["arguments"])
            function_response = function_arguments["answer"]

            

            with open('string.txt', 'r') as file:
                # Read all lines in the file
                lines = file.readlines()

                # Initialize tempOption as None (it will remain None if no matching line is found)
                tempOption = None

                # Loop over all lines
                for line in lines:
                    # Check if the line starts with 'function_response'
                    if line.startswith(function_response+":"):
                        # Extract the option from the line (assuming it's the next character)
                        tempOption = line
                        break

                            

            try:
                print("\n\n I think it's " , colored(tempOption.replace("\n",""),"red"), " with " , colored(function_arguments["certainty"],"green"), "%"," certainty because: \n", function_arguments["answerComplete"])
            except:
                print("\n\n I think it's " , colored(function_response,"red"), " with " , colored(function_arguments["certainty"],"green"), "%"," certainty because: \n", function_arguments["answerComplete"])

            

            self.messages.clear()
            self.messages = [{"role": "system", "content": "You are a quizz assistant in the game Rise of Kingdoms."}]

            # Switch case for reply A, B, C, D, or E
            if not self.midterm:
                # make function_arguments["certainty"] to int and see if its < 95
                if function_arguments["certainty"] >= 95:
                    if function_response == "E":
                        print("Not Sure")
                    elif function_response == "A":
                        ManualClickAction(40,48).execute()
                    elif function_response == "B":
                        ManualClickAction(60,50).execute()
                    elif function_response == "C":
                       ManualClickAction(40,58).execute()
                    elif function_response == "D":
                        ManualClickAction(60,58).execute()
                else:
                    print("")
                
            else:
                if function_arguments["certainty"] >= 95:
                    if function_response == "E":
                        print("Not Sure")
                    elif function_response == "A":
                        ManualClickAction(37,55).execute()
                    elif function_response == "B":
                        ManualClickAction(60,55).execute()
                    elif function_response == "C":
                        ManualClickAction(37,63).execute()
                    elif function_response == "D":
                        ManualClickAction(60,63).execute()
                

        
        time.sleep(2)
        os.system('cls')
        return True