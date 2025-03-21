import logging
import os
import time

import google.generativeai as genai
import asyncio

# Configure your Gemini API key
genai.configure(api_key="AIzaSyAa1HbCTRBpgnH_l_6b6sl26AccQikKc8w")

# Model to use (Gemini Pro in this case)
AI_COMPLETION_MODEL = "gemini-2.0-flash"
LANGUAGE = os.getenv("LANGUAGE", "hi-IN")
INITIAL_PROMPT = f"You are a versatile assistant. Respond to user queries in {LANGUAGE} or hinglish , handling Hinglish, interruptions, and ambiguous requests. Provide concise answers (3-4 sentences), maintain context, and adapt to changing user needs.  "

async def get_completion(user_prompt, conversation_thus_far):
    if _is_empty(user_prompt):
        raise ValueError("empty user prompt received")

    start_time = time.time()

    # Setup the model
    model = genai.GenerativeModel(AI_COMPLETION_MODEL)

    # Construct the prompt with the initial prompt, conversation history, and user prompt.
    prompt = f"{INITIAL_PROMPT}\n\n{conversation_thus_far}\nUser: {user_prompt}\nAssistant:"

    logging.debug("calling %s", AI_COMPLETION_MODEL)

    # Generate the response
    try:
        response = model.generate_content(prompt)

        completion = response.text
    except Exception as e:
        logging.error(f"Error generating content: {e}")
        return "An error occurred while processing your request." #Handle error and return a message.

    logging.info("response received from %s %s %s %s", AI_COMPLETION_MODEL, "in", time.time() - start_time, "seconds")
    logging.info('%s %s %s', AI_COMPLETION_MODEL, "response:", completion)

    return completion

def _is_empty(user_prompt: str):
    return not user_prompt or user_prompt.isspace()

#Example of how to use it.
async def main():
    conversation = "" # Initialize conversation history
    while True: # loop for multiple turns
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        try:
            result = await get_completion(user_input, conversation)
            print("Assistant:", result)
            # Update the conversation history
            conversation += f"User: {user_input}\nAssistant: {result}\n"
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())