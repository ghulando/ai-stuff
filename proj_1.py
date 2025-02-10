#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import openai

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

headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/117.0.0.0 Safari/537.36")
}

# ------------------------------------------------------------------------------
# Website Class
# ------------------------------------------------------------------------------

class Website:
    """
    A utility class to represent a Website that we have scraped,
    with its title, text content, and links.
    """
    def __init__(self, url: str):
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            self.body = response.content
            soup = BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            if soup.body:
                # Remove irrelevant tags
                for tag in soup.body(["script", "style", "img", "input"]):
                    tag.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
            # Extract all href values from anchor tags
            links = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            self.body = ""
            self.title = "Error fetching page"
            self.text = ""
            self.links = []

    def get_contents(self) -> str:
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# ------------------------------------------------------------------------------
# Functions for Link Extraction via OpenAI
# ------------------------------------------------------------------------------

# System prompt for the OpenAI call that filters the website links
link_system_prompt = (
    "You are provided with a list of links found on a webpage. "
    "You are able to decide which of the links would be most relevant to include in a brochure about the company, "
    "such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
    "You should respond in JSON as in this example:\n"
    "{\n"
    '    "links": [\n'
    '        {"type": "about page", "url": "https://full.url/goes/here/about"},\n'
    '        {"type": "careers page", "url": "https://another.full.url/careers"}\n'
    "    ]\n"
    "}\n"
)

def get_links_user_prompt(website: Website) -> str:
    """
    Creates the user prompt string for the link-filtering OpenAI call.
    """
    prompt = (f"Here is the list of links on the website of {website.url} - "
              "please decide which of these are relevant web links for a brochure about the company, "
              "respond with the full https URL in JSON format. Do not include Terms of Service, Privacy, or email links.\n"
              "Links (some might be relative links):\n")
    prompt += "\n".join(website.links)
    return prompt

def get_links(url: str) -> dict:
    """
    Given a URL, scrape the page, extract its links, and use OpenAI to decide which are relevant.
    Returns the parsed JSON response.
    """
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ]
    )
    result = response.choices[0].message.content
    print("OpenAI Response:", result)  # Debug line to see the raw response
    try:
        return json.loads(result)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        # Return a default empty structure if JSON parsing fails
        return {"links": []}

# ------------------------------------------------------------------------------
# Functions for Brochure Generation
# ------------------------------------------------------------------------------

def get_all_details(url: str) -> str:
    """
    Aggregates details from the landing page and additional pages (based on selected links)
    to be used for generating the brochure.
    """
    details = "Landing page:\n"
    details += Website(url).get_contents()
    links = get_links(url)
    print("Found links:", links)  # Debug output to show the JSON structure returned
    for link in links["links"]:
        time.sleep(1)  # Add a 1-second delay between requests
        details += f"\n\n{link['type']}\n"
        details += Website(link["url"]).get_contents()
    return details

# System prompt for creating the brochure. (You can switch to a humorous tone by changing this prompt.)
system_prompt = (
    "You are an assistant that analyzes the contents of several relevant pages from a company website "
    "and creates a short brochure about the company for prospective customers, investors and recruits. "
    "Respond in markdown. Include details of company culture, customers and careers/jobs if you have the information."
)

def get_brochure_user_prompt(company_name: str, url: str) -> str:
    """
    Creates the full user prompt for the brochure-generation OpenAI call.
    """
    prompt = f"You are looking at a company called: {company_name}\n"
    prompt += ("Here are the contents of its landing page and other relevant pages; "
               "use this information to build a short brochure of the company in markdown.\n")
    prompt += get_all_details(url)
    # Truncate if longer than 5000 characters (to avoid hitting prompt limits)
    return prompt[:5000]

def create_brochure(company_name: str, url: str):
    """
    Creates and prints the brochure using a standard (non-streaming) OpenAI call.
    """
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )
    result = response.choices[0].message.content
    print("\n=== Generated Brochure ===\n")
    print(result)

def stream_brochure(company_name: str, url: str):
    """
    Streams the generated brochure content from OpenAI.
    """
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ],
        stream=True
    )
    
    print("\n=== Streaming Brochure ===\n")
    for chunk in stream:
        delta = chunk.choices[0].delta
        if 'content' in delta:
            content = delta.content
            sys.stdout.write(content)
            sys.stdout.flush()
    print()  # Add a newline after streaming

# ------------------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------------------

def main():
    # Get company name and URL from command line arguments or environment variables
    company_name = os.getenv('COMPANY_NAME', 'edward donner')
    url = os.getenv('COMPANY_URL', 'https://edwarddonner.com')
    
    # Use streaming by default, but allow override
    use_streaming = os.getenv('USE_STREAMING', 'false').lower() == 'true'
    
    if use_streaming:
        stream_brochure(company_name, url)
    else:
        create_brochure(company_name, url)

if __name__ == '__main__':
    main()
