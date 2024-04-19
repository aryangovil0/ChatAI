'''
Created by Aryan Govil, 2024

'''
#!/usr/bin/env python3

import os
import subprocess
import sys
import time
import textwrap
import shutil

from utils import Color, get_valid_input, print_green_divider, chat_interaction
from groq import Groq

os.system('cls' if os.name == 'nt' else 'clear')

print()
groq = Color.RED + "   ___                    __ _             ___    _                _     \n" \
       "  / __|     _ _    ___   / _` |           / __|  | |_     __ _    | |_   \n" \
       " | (_ |    | '_|  / _ \\  \\__, |     _    | (__   | ' \\   / _` |   |  _|  \n" \
       "  \\___|   _|_|_   \\___/   __|_|   _(_)_   \\___|  |_||_|  \\__,_|   _\\__|  \n" \
       "_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"|_|\"\"\"\"\"| \n" \
       "`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'\"`-0-0-'" + Color.RESET

chat = Color.WHITE + Color.RESET
print(groq + chat)
print("\n\n")
print(Color.PURPLE_BOLD + "Created by Aryan Govil" + Color.RESET)
print()
print(Color.RED_BOLD + "Powered by Groq LPU" + Color.RESET)
print(Color.ORANGE + "Model: llama3-8b-8192" + Color.RESET)
print()

def main():
    api_key = os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("API key not found. Please set the GROQ_API_KEY environment variable and try again.")
        return
    
    client = Groq(api_key=api_key)
    
    while True:
        # Prompt the user for temperature and max tokens within the allowed ranges
        temperature = get_valid_input("Enter the temperature (0.0 to 2.0): ", 0.0, 2.0)
        if temperature == '/reset':
            continue
        max_tokens = get_valid_input("Enter the max tokens (Mixtral = 32768, Llama = 4096): ", 1, 32768, is_float=False)
        if max_tokens == '/reset':
            continue
        
        # Start chat
        reset_requested = chat_interaction(client, temperature, max_tokens)
        
        if reset_requested:
            print("Resetting...\n")
            python_executable = sys.executable  # Get the path to the Python interpreter
            subprocess.call([python_executable, sys.argv[0]])  # Restart the script
            sys.exit()  # Exit the current instance of the script

if __name__ == '__main__':
    main()