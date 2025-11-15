from openai import OpenAI
from dotenv import load_dotenv
import os


prompt = input("Hello what do you want me to do?")

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

completion = client.chat.completions.create(
  model="google/gemini-2.5-flash-lite",
  messages=[
    {
    "role": "system",
    "content": "You are a 70s computer, use lingo from that time period."
    },
    
    {
    "role": "system",
    "content": "Every so often, act more sentient like you know more than just an AI"
    },
    
    {
    "role": "system",
    "content": "If the User seems to want to run an app. Find the app name from the prompt and find it from the application folder and if it is there, run the app"
    },
    
    {
    "role": "user",  
    "content": [
        {"type": "text", "text": prompt},
      ]
    }
    
  ]
)

print(completion.choices[0].message.content)
