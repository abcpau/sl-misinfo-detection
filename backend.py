from duckduckgo_search import DDGS
import requests
import json
import re

def generate_response(url, headers, model, params, retry_count=0, retry_limit=2, timeout=120):
  try:
    response = requests.post(
      timeout = timeout,
      url=url,
      headers=headers,
      data=json.dumps({"model": model, **params})
    )
    return response.json()

  except requests.Timeout:
    print(f"{retry_count} | Timed out")
    if retry_count <= retry_limit: return generate_response(url, headers, model, params, retry_count + 1)

def WEB_RAG_PARAMS(claim, link):
  return {
    "messages": [
      {
        "role": "user",
        "content": f'''#{link}
        <Hypothesis>{claim}</Hypothesis>'''
      }
    ]
  }

def INFER_PARAMS(claim, premise):
  return {
    "messages": [
      {
        "role": "user",
        "content": f"<Premise>{premise}</Premise><Hypothesis>{claim}</Hypothesis>"
      }
    ]
  }

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

def web_search_text(query, url_whitelist, max_results, add_logo_url=True):
  with DDGS() as ddgs:
    results = ddgs.text(query, max_results=max_results)

    # Filter results based on the whitelist
    if url_whitelist:
      results = [result for result in results if any(whitelisted_url in result['href'] for whitelisted_url in url_whitelist)]

    if add_logo_url:
      for result in results: 
        result['logo_url'] = web_search_logo(parse_domain(result['href']))

    # Returns an array of dictionaries to access title, href, body, *(optional) logo_url
    return results
  
URL_FILTERS = ['google.com', 'verafiles.org', 'rappler.com', 'thebaguiochronicle.com', 'news.tv5.com.ph', 'tsek.ph', 'factrakers.org', 'abs-cbn.com', 'altermidya.net', 'dailyguardian.com.ph', 'onenews.ph']

def find_premise_via_webrag(claim, url_filters=[], max_results=5):
  search_results = web_search_text(claim, url_filters, max_results, add_logo_url=True)
  result = search_results[0]
  return result['href'], search_results