import requests
import json

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