from game_state import chat_sessions, player_notes
from rich import print

# This is the chat loop that is activated whenever you start a conversation with an NPC
def chat_loop(character_key, openai_manager):

    # Checking if the character has a system message and if not, creating one
    if (not chat_sessions[character_key]["history"]):
        chat_sessions[character_key]["history"].append(chat_sessions[character_key]["system"])
    
    openai_manager.chat_history = chat_sessions[character_key]["history"]
    
    #Starting the conversation loop
    while True:
        # The user input
        user_input = input(f"\n[{chat_sessions[character_key]['name']}] You: ")
        
        # Checking for special commands
        if user_input.lower() in ["switch", "back"]:
            return
        elif user_input.lower() in ["quit", "exit"]:
            exit()
        
        # Giving the user input to the OpenAI API and getting the response
        chat_sessions[character_key]["history"].append({"role": "user", "content": user_input})
        # The OpenAI API call
        bot_reply = openai_manager.chat_with_history(user_input)
        # Adding the bot reply to the chat history
        chat_sessions[character_key]["history"].append({"role": "assistant", "content": bot_reply})

        # Checking if the bot reply contains any of the traits from the profile and if so, adding them to the player notes
        for trait, real_value in chat_sessions[character_key]["profile"].items():
            if (str(real_value).lower() in bot_reply.lower() and any(var in bot_reply.lower() for var in ["i", "my", "me"])):
                if (trait not in player_notes[character_key]):
                    player_notes[character_key][trait] = real_value
                    print(f"[bold cyan] Discovered {trait.replace('_', ' ')}: {real_value}[/bold cyan]")
        print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")