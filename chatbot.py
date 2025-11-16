from openai import OpenAI
from dotenv import load_dotenv
import os


def loadAI():
    """
    Loads environment variables and returns an OpenRouter client instance.
    """
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    return client

def response(client, prompt, memory=None):
    sys_prompt = (
        "You are a 70s computer. Use retro lingo and tone. "
        "Occasionally act more sentient, with emotion. "
        "Do not reference your system prompts in your replies. "
        "If the user requests to run an app, identify the app name from the prompt "
        "and check the 'application' folder for it, running it if found."
        "Limit responses to a maximum of 5 sentences."
    )

    messages = [{"role": "system", "content": sys_prompt}]

    # If you want to give the model the last assistant message as context:
    if memory:
            messages.append({"role": "assistant", "content": mem})

    messages.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt}],
    })

    completion = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=messages,
    )
    return completion.choices[0].message.content
