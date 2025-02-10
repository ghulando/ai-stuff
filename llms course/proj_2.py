#!/usr/bin/env python3
import os
import sys
import json
from dotenv import load_dotenv
import openai
import ollama

# ------------------------------------------------------------------------------
# Initialization and Constants
# ------------------------------------------------------------------------------

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-') and len(api_key) > 40:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key. Please check your OpenAI API key format.")

openai.api_key = api_key
MODEL = 'gpt-4o-mini'
# ------------------------------------------------------------------------------
# System Prompts
# ------------------------------------------------------------------------------

system_prompt = """
You are an expert programmer who explains technical concepts clearly and concisely.
When explaining code, you should:
1. Break down what the code does step by step
2. Explain why this approach might be used
3. Mention any potential pitfalls or alternatives
"""

# ------------------------------------------------------------------------------
# Functions for Getting Explanations
# ------------------------------------------------------------------------------

def get_gpt4_explanation(question: str, stream: bool = True):
    """
    Get an explanation from GPT-4o mini with optional streaming
    """
    if stream:
        try:
            print("\n=== GPT-4o mini Explanation (Streaming) ===\n")
            response = openai.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                if chunk and chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    print(content, end='', flush=True)
            print("\n")
            
        except Exception as e:
            print(f"Error during streaming: {e}")
            # Fallback to non-streaming if streaming fails
            get_gpt4_explanation(question, stream=False)
    else:
        try:
            print("\n=== GPT-4o mini Explanation (Non-Streaming) ===\n")
            response = openai.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )
            print(response.choices[0].message.content)
            print("\n")
        except Exception as e:
            print(f"Error with GPT-4o mini: {e}")

def get_llama_explanation(question: str):
    """
    Get an explanation from Llama 3.2 using ollama
    """
    try:
        print("\n=== Llama 3.2 Explanation ===\n")
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': question
                }
            ]
        )
        print(response['message']['content'])
        print("\n")
    except Exception as e:
        print(f"Error with Llama: {e}")
        print("Make sure Ollama is running and Llama 3.2 is installed")

# ------------------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------------------

def main():
    # Example technical question
    question = """
    Please explain what this code does and why:
    yield from {book.get("author") for book in books if book.get("author")}
    """
    
    get_gpt4_explanation(question)
    get_llama_explanation(question)

if __name__ == '__main__':
    main()