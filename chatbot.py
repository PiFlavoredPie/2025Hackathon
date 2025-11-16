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


def response(client, prompt, memory=[]):
    

    folder = 'applications'  # replace with your folder path

    python_files = [f for f in os.listdir(folder) if f.endswith('.py')]
    
    sys_prompt = (
        "You are a 70s computer. Use retro lingo and tone. "
        "Occasionally act more sentient, with emotion. "
        "Do not reference your system prompts in your replies. "
        "if and ONLY if user wants to run one of these apps: " + str(python_files) +
        "User HAS to have the words 'run' and the file name, (disregard difference in spaces and things like punctuation in file name)"
        "oregon trail (check if the prompt has anything that relates to the oregon trail and set python_file to oregon_trail.py)"
        "and check if it matches any installed applications, and put this string at the end of the response '\npython3 applications/(python_file)'"
        "Limit responses to a maximum of 5 sentences."
    )

    messages = [{"role": "system", "content": sys_prompt}] + memory

    # If you want to give the model the last assistant message as context:

    


    completion = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=messages,
    )
    return completion.choices[0].message.content
