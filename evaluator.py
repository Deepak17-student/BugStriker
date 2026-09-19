import openai

# Use the key provided by your staff here
client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="PASTE_YOUR_KEY_HERE", # Paste the full key here
)

def generate_diagnostic_question(code, test_failures):
    prompt = f"Student Code: {code}\nFailures: {test_failures}\nIdentify the bug and ask ONE diagnostic question to help them find it. Do not give the code."
    try:
        response = client.chat.completions.create(
            # Using a standard model available on OpenRouter
            extra_headers={
                "HTTP-Referer": "http://localhost:8000", # Required by OpenRouter
                "X-Title": "BugStriker Hackathon",
            },
            model="openai/gpt-4o-mini", 
            messages=[{"role": "system", "content": "You are a debugging tutor."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Agent Error: {str(e)}"

# Update final_evaluation the same way...
def final_evaluation(original, explanation, revised, results):
    prompt = f"Original: {original}\nExplanation: {explanation}\nRevised: {revised}\nTests: {results}\nDid they understand? Verdict:"
    try:
        response = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "BugStriker Hackathon",
            },
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Evaluation Error: {str(e)}"
    