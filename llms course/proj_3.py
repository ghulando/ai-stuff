import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from IPython.display import Markdown, display, update_display

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    exit()
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")
    exit()

client = OpenAI(api_key=openai_api_key)
claude = anthropic.Anthropic(api_key=anthropic_api_key)

system_message = "You are an assistant that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
]

print("\n" + "="*50)
print("Requesting response from OpenAI GPT-4...")
print("="*50 + "\n")

completion = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=prompts,
    temperature=0.7
)
print(completion.choices[0].message.content)

print("\n" + "="*50)
print("OpenAI response completed")
print("="*50 + "\n")

print("\n" + "="*50)
print("Requesting response from Anthropic Claude...")
print("="*50 + "\n")

result = claude.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    temperature=0.7,
    system=system_message,
    messages=[
        {"role": "user", "content": user_prompt},
    ],
)

with result as stream:
    for text in stream.text_stream:
            print(text, end="", flush=True)

print("\n" + "="*50)
print("Claude response completed")
print("="*50)