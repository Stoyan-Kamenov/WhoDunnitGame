from character import generate_random_profile, generate_system_message, PERSONALITY_POOL, POSSIBLE_IDENTITIES
import random

random.shuffle(POSSIBLE_IDENTITIES)

# The possible murder cases
MURDER_CASES = [
    "Early in the morning Geraldine Thomas was discovered deceased in her LA residence, her face had taken a beating but the cause of death was strangulation.",
    "Last night at the horseshoe pier, a dame named Sally Foot was found dead with several pistol rounds in her back.",
    "On Halloween a movie star by the name of Glock Steward was found dead, half submerged in the tar pits, the only wound he had was a stab wound in his chest.",
    "Late last night the star pitcher for the LA Angels, Red Osbourne was found dead in a dope shop, his head was smashed barely even recognizable.",
    "Tom Dillenger a politician top runner for the next mayoral race, was discovered by some kids behind the LA sign, though his head was no longer attached to his body."
]

# The clue traits given out
CLUE_TRAITS = ["height", "build", "gender", "hair_colour", "facial_hair", "hair_length"]

# The character keys
character_keys = ["Suspect 1", "Suspect 2", "Suspect 3", "Suspect 4"]

chat_sessions = {}

# Generating the random character
for key in character_keys:
    name, description = POSSIBLE_IDENTITIES.pop()
    chat_sessions[key] = {
        "name": name,
        "description": description,
        "system": {},
        "history": [],
        "profile": generate_random_profile(),
        "personality": random.choice(PERSONALITY_POOL),
        "is_murderer": None
    }

player_notes = {key: {} for key in chat_sessions.keys()}

# Giving each character a clue in the system message 
def assign_clues(murderer_key):
    available_traits = CLUE_TRAITS.copy()
    innocent_keys = [key for key in chat_sessions if key != murderer_key]
    random.shuffle(innocent_keys)
    random.shuffle(available_traits)
    for bot_key, trait in zip(innocent_keys, available_traits):
        trait_value = chat_sessions[murderer_key]["profile"][trait]
        chat_sessions[bot_key]["witness_clue"] = (trait, trait_value)

# Assigning the framing target for the murderer
def assign_framing_target(murderer_key):
    innocents = [k for k in chat_sessions if k != murderer_key]
    framed_key = random.choice(innocents)
    chat_sessions[murderer_key]["framing_target"] = chat_sessions[framed_key]["name"]
    chat_sessions[murderer_key]["framing_profile"] = chat_sessions[framed_key]["profile"]

# Assigning the murderer
def assign_murderer(murder_case):
    chosen = random.choice(list(chat_sessions.keys()))
    assign_clues(chosen)
    assign_framing_target(chosen)
    for key in chat_sessions:
        # Checking if its the murderer and giving it special conditions
        is_murderer = (key == chosen)
        chat_sessions[key]["is_murderer"] = is_murderer
        if (is_murderer):
            chat_sessions[key].pop("personality", None)
            personality = None
        else:
            personality = chat_sessions[key]["personality"]
        
        # Generating the system message
        chat_sessions[key]["system"] = generate_system_message(
            chat_sessions[key]["name"],
            chat_sessions[key]["description"],
            chat_sessions[key]["profile"],
            is_murderer,
            murder_case,
            chat_sessions[key].get("witness_clue", None),
            chat_sessions[key].get("framing_target", None),
            chat_sessions[key].get("framing_profile", None),
            personality
        )