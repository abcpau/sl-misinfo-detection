from duckduckgo_search import DDGS
import requests
import json
import re

def format_premise_hypothesis(premise, hypothesis):
  return f"<Premise>{premise}</Premise><Hypothesis>{hypothesis}</Hypothesis>"

def generate_inference(url, headers, model, content, retry_count=0, retry_limit=2, timeout=120):
  try:
    response = requests.post(
      timeout = timeout,
      url=url,
      headers=headers,
      data=json.dumps({
        "model": model,
        "temperature": 0,
        "options": {"temperature": 0},
        "stream": False,
        "messages": [
          {
            "role": "system",
            "content": "You are an investigator who is an expert at inference. You check if the given <Premise> ENTAILS, CONTRADICTS, or IS NEUTRAL TO the given <Hypothesis>. If the <Premise> ENTAILS the <Hypothesis>, say 'fact' followed by an explanation why. If the <Premise> CONTRADICTS or IS NEUTRAL TO the <Hypothesis>, say 'false' followed by an explanation why. Use the format '{fact/false} - {explanation}'.",
          },
          {
            "role": "user",
            "content": content
          }
        ]
    }))
    return response.json()["message"]["content"]

  except requests.Timeout:
    print(f"{retry_count} | Timed out")
    if retry_count <= retry_limit: return generate_inference(url, headers, model, content, retry_count + 1)
    
def parse_llama_explanation(text):
  try:
    label, explanation = text.split(' - ')
    return label, explanation
    # return label, text                    # DEBUG
  except Exception as e:
    print(f"Error: {e}")
    return 'error', text

def parse_domain(link):
  think_pattern = r"https://(?:www\.)?([^/]+)"
  re_match = re.search(think_pattern, link, re.DOTALL)
  web_link = re_match.group(1).strip()
  return web_link

def web_search_logo(query):
  with DDGS() as ddgs:
    results = ddgs.images(f"{query} logo", max_results=1)  # Get the first image

    if results:
      # Returns logo URL
      return results[0]['image']

    raise ValueError("No image found.")

def web_search_text(query, max_results=3, add_logo_url=True):
  with DDGS() as ddgs:
    results = ddgs.text(query, max_results=max_results)  # Get the top 5 results

    if add_logo_url:
      for result in results: result['logo_url'] = web_search_logo(parse_domain(result['href']))

    # Returns an array of dictionaries to access title, href, body, *(optional) logo_url
    return results

def find_premise_via_webrag(claim, url_filters):
  search_results = web_search_text(claim, max_results=1)
  result = search_results[0]

  return result['href'], search_results