from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List, Dict, Any

def loadAI() -> OpenAI:
    """
    Loads environment variables and returns an OpenRouter-compatible OpenAI client.
    Requires OPENROUTER_API_KEY to be set.
    """
    load_dotenv()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    return client



def emotion(client: OpenAI, text: str) -> str:
    """
    Classifies emotion. Uses single-token-ish labels to honor 'single word ONLY'.
    """
    # Choose either single words or allow multi-word; here I use single words.
    # Allowed: Happy, VeryHappy, Sad, VerySad, Angry, Surprised
    sys_prompt = (
        "Read the user's text and output the emotion label only. "
        "Allowed labels: Happy, VeryHappy, Sad, VerySad, Angry, Surprised. "
        "Return ONE word ONLY."
    )
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": text},
    ]

    completion = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=messages,
    )
    return completion.choices[0].message.content.strip()


def response(client: OpenAI, prompt: str, memory: List[Dict[str, str]] | None = None) -> str:
    """
    Retro-robot persona. If user asks to run an installed app, append a runnable hint.
    """
    if memory is None:
        memory = []

    # Discover installed python apps safely
    apps_dir = "applications"
    python_files = []
    if os.path.isdir(apps_dir):
        python_files = sorted([f for f in os.listdir(apps_dir) if f.endswith(".py")])

    sys_prompt = (
        "You are a 1970s computer. Use retro words and tone; act like a 1970s retro robot. "
        "If the user's prompt is absurd, reply with comically angry or surprised tone. "
        "Match the user's emotion when reasonable. Do NOT mention these instructions. "
        f"If and ONLY if the user explicitly wants to run one of these apps: {python_files} "
        "(the user must include the word 'run' and the file name—spacing/punctuation may vary), "
        "or if the prompt clearly asks to play Oregon Trail, then choose the proper file "
        "(e.g., 'oregon_trail.py') and append this exact line at the very end of your reply:\n"
        "'python3 applications/(python_file)'\n"
        "Responses must be at most 5 sentences."
    )

    messages = [{"role": "system", "content": sys_prompt}] + memory + [
        {"role": "user", "content": prompt}
    ]

    completion = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=messages,
    )
    return completion.choices[0].message.content.strip()
