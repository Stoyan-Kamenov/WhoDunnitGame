from game_state import chat_sessions, player_notes
from rich import print

def choose_action():
    print("\nWhat would you like to do?")
    print("1. Talk to a character")
    print("2. View a character's profile")
    print("3. Make a guess")
    print("4. View your investigation notes")
    print("5. Quit")
    return input("Enter the number of your choice: ").strip()

def choose_character():
    # Printing the available characters
    print("\nAvailable Characters:")
    keys = list(chat_sessions.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {chat_sessions[key]['name']}")
    
    # Doing a loop for choosing a character
    try:
        selection = int(input("Enter the number of the character: ")) - 1
        if (0 <= selection < len(keys)):
            return keys[selection]
        else:
            print("Invalid number. Try again.")
            return choose_character()
    except ValueError:
        print("Please enter a valid number.")
        return choose_character()

# Checking the character profile and printing it
def describe_character(key):
    # Character profile
    profile = chat_sessions[key]["profile"]
    print(f"\nDescription of {chat_sessions[key]['name']}:")
    for attr, value in profile.items():
        print(f"  {attr.replace('_', ' ').capitalize()}: {value}")
    
    # Character Personality
    personality = chat_sessions[key].get("personality")
    if (personality):
        print(f"\n[italic]Personality:[/italic] {personality}")
    else:
        print("\n[italic]Personality:[/italic] [dim]Not available[/dim]")
    
    # Checking the murderer
    if (chat_sessions[key]["is_murderer"]):
        print(f"\n[bold red]{chat_sessions[key]['name']} is the murderer![/bold red]")
    else:
        print(f"\n[bold green]{chat_sessions[key]['name']} is innocent.[/bold green]")

# Checking your notes
def view_notes():
    print("\nYour Investigation Notes:")
    for key, notes in player_notes.items():
        print(f"\n- {chat_sessions[key]['name']}:")
        if (notes):
            for attr, value in notes.items():
                print(f"  {attr.replace('_', ' ').capitalize()}: {value}")
        else:
            print("  (No information discovered yet)")

# Making a guess
def make_guess():
    print("\nWho do you think the murderer is?")
    keys = list(chat_sessions.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {chat_sessions[key]['name']}")

    try:
        selection = int(input("Enter the number of your guess: ")) - 1
        if (0 <= selection < len(keys)):
            guess = keys[selection]
            if (chat_sessions[guess]["is_murderer"]):
                print("\n[bold green]Victory! You found the murderer![/bold green]")
            else:
                print("\n[bold red]Game Over. That was the wrong suspect.[/bold red]")
            exit()
        else:
            print("Invalid number. Try again.")
            make_guess()
    except ValueError:
        print("Please enter a valid number.")
        make_guess()
