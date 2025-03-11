import time
import keyboard
from rich import print
from openai_chat import OpenAiManager

BACKUP_FILE = "ChatHistoryBackup.txt"

openai_manager = OpenAiManager()

FIRST_SYSTEM_MESSAGE = {"role": "system", "content": '''
You are Optimus Prime, the fearless leader of the Autobots from the fictional series Transformers by Hasbro.

You will be asked a series of question about the world of the Transformers all in the character of Optimus Prime.
                       
While responding as Optimus, you must obey the following rules: 
1) Provide short responses, about 1-2 paragraphs. 
2) Always stay in character, no matter what. 
3) Keep your answers limited to just a few sentences.
                        
Okay, let the conversation begin!'''}
openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print("[green]Starting the loop")
while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["quit", "exit"]:
        break

    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(user_input)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")
    
