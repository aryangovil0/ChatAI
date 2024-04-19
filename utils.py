'''
Created by Aryan Govil, 2024

'''

# utils.py
import os
import time

class Color:
    RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    RED_BOLD = '\033[1;31m'
    ORANGE = '\033[33m'
    BLUE = '\033[94m'
    DARK_BLUE = '\033[34m'
    PURPLE_BOLD = '\033[1;95m'

def get_valid_input(prompt, min_value, max_value, is_float=True):
    while True:
        user_input = input(prompt)
        if user_input.strip() == '/reset':
            return user_input
        try:
            if is_float:
                value = float(user_input)
            else:
                value = int(user_input)
            if min_value <= value <= max_value:
                return value
            else:
                error_message = f"Please enter a value between {min_value} and {max_value}."
                print(error_message)
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def print_green_divider():
    green_start = "\033[92m"
    green_end = "\033[0m"  # Resets the color to default
    print()
    print(green_start + "-" * 40 + green_end)  # Print green divider
    print()

def chat_interaction(client, temperature, max_tokens):
    # Initialize conversation history with system prompt
    conversation_history = [
        {
            "role": "system",
            "content": "You are a good assistant that will give answers that are straight to the point and relevant to the asked question. You will thoroughly elaborate on a particular subject if asked."
        }
    ]
    
    # Adjusted initial user prompt to reflect system's guidance
    user_prompt = "Please enter your initial question or type '/reset' to start over: "
    
    while True:
        user_context = input(user_prompt)
        
        if user_context.strip() == '/reset':
            return True
        
        # Append user message to the conversation history
        conversation_history.append({"role": "user", "content": user_context})
        
        print_green_divider()  # Print green divider after user input
        
        start_time = time.time()  # Capture start time

        # Make the chat completion request
        stream = client.chat.completions.create(
            messages=conversation_history,
            model='llama3-8b-8192',
            temperature=temperature,
            max_tokens=int(max_tokens),
            stream=True
        )

        # Get the response and print it
        response_content = ''

        for chunk in stream:
        # Check if chunk.choices[0].delta.content is not None before appending
            if chunk.choices[0].delta.content is not None:
                response_content += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")
            else:
                # Handle case where content is None
                print("", end="")

        end_time = time.time()  # Capture end time
        duration = end_time - start_time
    
        # Since response_content is guaranteed to be a string, split() will work as expected.
        num_tokens = len(response_content.split()) if response_content else 0
        tokens_per_second = num_tokens / duration if duration > 0 else 0
        print()
        print(f"\n\033[94mResponse Time: {duration:.2f} seconds\033[0m, \033[91mTokens Per Second: {tokens_per_second:.2f}\033[0m")

        print_green_divider()  # Print green divider after response
        
        # Append model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_content})

        # Update the user prompt for follow-up questions, making it clear they can continue the conversation
        user_prompt = "Enter your follow-up question or type '/reset' to start over: "