import google.generativeai as genai
import requests, json

GEMINI_KEY = "AIzaSyDiK57d7ReTzNYMlsr20oMEHrwaQZIYG74"
GATEWAY = "https://intent-protocol-xi.vercel.app/api/intent"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def process(prompt):
    # Prompt for structure
    system_prompt = (
        "Convert the user's request into a JSON object with exactly these fields:\n"
        '"action": one of "book","buy","find","compare"\n'
        '"target": the thing they want (e.g., "flight", "hotel", "laptop")\n'
        '"params": any details like origin, destination, date, product (as a JSON object)\n'
        '"constraints": max_price, preferred_providers, etc.\n'
        "Respond ONLY with the JSON, no other text."
    )
    full_prompt = f"{system_prompt}\n\nUser: {prompt}\nJSON:"
    
    response = model.generate_content(full_prompt)
    # Extract JSON from response (strip potential markdown code fences)
    raw = response.text.strip()
    if raw.startswith('```'):
        raw = raw.split('\n', 1)[1].rsplit('```', 1)[0]
    intent = json.loads(raw)
    
    # Send to gateway
    resp = requests.post(GATEWAY, json=intent)
    return resp.json()

if __name__ == '__main__':
    test = "Find me a hotel in Paris under $200"
    result = process(test)
    print(json.dumps(result, indent=2))
