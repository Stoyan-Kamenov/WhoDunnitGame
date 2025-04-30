from game_state import chat_sessions, player_notes
from rich import print

def chat_loop(character_key, openai_manager):
    if not chat_sessions[character_key]["history"]:
        chat_sessions[character_key]["history"].append(chat_sessions[character_key]["system"])
    openai_manager.chat_history = chat_sessions[character_key]["history"]
    while True:
        user_input = input(f"\n[{chat_sessions[character_key]['name']}] You: ")
        if user_input.lower() in ["switch", "back"]:
            return
        elif user_input.lower() in ["quit", "exit"]:
            exit()
        chat_sessions[character_key]["history"].append({"role": "user", "content": user_input})
        bot_reply = openai_manager.chat_with_history(user_input)
        chat_sessions[character_key]["history"].append({"role": "assistant", "content": bot_reply})
        for trait, real_value in chat_sessions[character_key]["profile"].items():
            if str(real_value).lower() in bot_reply.lower() and any(w in bot_reply.lower() for w in ["i", "my", "me"]):
                if trait not in player_notes[character_key]:
                    player_notes[character_key][trait] = real_value
                    print(f"[bold cyan]📝 Discovered {trait.replace('_', ' ')}: {real_value}[/bold cyan]")
        print("[green]\n!!!!!!!\nFINISHED PROCESSING DIALOGUE.\nREADY FOR NEXT INPUT\n!!!!!!!\n")