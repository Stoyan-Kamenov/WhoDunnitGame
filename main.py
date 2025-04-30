from game_state import assign_murderer, MURDER_CASES
from ui import choose_action, choose_character, describe_character, make_guess, view_notes
from chat_loop import chat_loop
from openai_integration import OpenAiManager
import random
from rich import print

def main():
    # Getting connection to the API
    openai_manager = OpenAiManager()

    # Chosing the current case and printing it
    current_case = random.choice(MURDER_CASES)
    print(f"\n[bold red]Murder Case:[/bold red] {current_case}")
    
    # Assinging the murderer and specific values neded
    assign_murderer(current_case)

    # Main Menu loop
    while True:
        action = choose_action()
        if action == "1":
            character_key = choose_character()
            chat_loop(character_key, openai_manager)
        elif action == "2":
            character_key = choose_character()
            describe_character(character_key)
        elif action == "3":
            make_guess()
        elif action == "4":
            view_notes()
        elif action == "5":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Try again.")

if (__name__ == "__main__"):
    main()