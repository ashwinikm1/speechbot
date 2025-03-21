import logging
import os
import time

import google.generativeai as genai
import asyncio

# Configure your Gemini API key
genai.configure(api_key="")

# Model to use (Gemini Pro in this case)
AI_COMPLETION_MODEL = "gemini-2.0-flash-lite-001"
LANGUAGE = os.getenv("LANGUAGE", "hi")
INITIAL_PROMPT = f"You are a versatile assistant. Respond to user queries in {LANGUAGE} or hindi , handling Hinglish, interruptions, and ambiguous requests. Provide concise answers (3-4 sentences), maintain context, and adapt to changing user needs.  "

async def get_completion(user_prompt, conversation_thus_far):
    if _is_empty(user_prompt):
        raise ValueError("empty user prompt received")

    start_time = time.time()

    # Setup the model
    model = genai.GenerativeModel(AI_COMPLETION_MODEL)

    # Construct the prompt with the initial prompt and user prompt.
    prompt = f"{INITIAL_PROMPT}\n\n{user_prompt}"

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
    user_input = "What is the capital of France?"
    conversation = "" #Not used in this example, but can be implemented.

    try:
        result = await get_completion(user_input, conversation)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
