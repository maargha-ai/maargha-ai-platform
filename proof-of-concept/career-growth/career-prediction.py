import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("career-growth"))

# Questions
QUESTIONS = [
    "Do you enjoy solving mathematical problems? (yes/no)",
    "Are you interested in cybersecurity or ethical hacking? (yes/no)",
    "Do you find networking, servers, infrastructure appealing? (yes/no)",
    "Do you like writing code and building software? (yes/no)",
    "Are you intrested in databases and data engineering? (yes/no)",
    "Do you enjoy machine learning or AI research? (yes/no)",
    "Do you prefer working on UI/UX and front-end design? (yes/no)",
    "Do you like debugging and maintaining production systems? (yes/no)",
    "Would you enjoy customer-facing and business-oriented IT roles? (yes/no)",
    "Would you like roles involving statistics and analytics? (yes/no)",
    "Do you like research-focused roles that explore new AI techniques? (yes/no)",
    "Does Linux system administration excite you? (yes/no)",
    "Does forensic analysis of cyber attacks excite you? (yes/no)",
    "Do you prefer mobile development (Android/iOS) or web UI? (yes/no)",
    "Do you enjoy detecting edge cases and breaking applications? (yes/no)",
    "Do you enjoy configuring routers, switches and firewalls? (yes/no)",
    "Are you interested in game engines like Unity or Unreal Engine? (yes/no)",
    "Would you enjoy a role in teaching, mentorship, or educational content creation? (yes/no)",
    "How much time daily can you commit to learning? (hours/day)"
]

# Prompt Builder
def build_prompt(answers: dict) -> str:
    bullet_text = "\n".join([f"- {q}: {a}" for q, a in answers.items()])

    return f"""
    You are an expert IT career advisor.quit

    Based on the user's answers, recommend EXACTLY 4 suitable IT careers.
    For each career provide:
    1. Title (example: "Data Engineer")
    2. One-line reason why it matches the user
    3. Top 5 skills to learn

    User responses:
    {bullet_text}

    Resopnd ONLY in valid JSON as a list of objects:
    [
    {{
        "title": "...",
        "reason": "...",
        "skills": [...]
    }}
    ]
    """

# LLM call
def call_llm(prompt: str)->str:
    response = client.chat.completions.create(
        model="llama-3.3-70B-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200
    )

    return response

# Run interactive assessment
def run_career_prediction():
    print("\n==== IT Career Predictor ====n")
    answers = {}

    # ask questions interactively 
    for q in QUESTIONS:
        ans = input(q + "\n> ")
        answers[q] = ans

    # create LLM prompt
    prompt = build_prompt(answers)

    # call LLM
    print("\nGenerating career suggestions...\n")
    response = call_llm(prompt)

    # parse and print result
    result_json = response.choices[0].message.content
    careers = json.loads(result_json)  # Convert string to Json format

    print(" Recommended Careers \n")

    for c in careers:
        
        print(f"Career: {c['title']}")
        print(f"Reason: {c['reason']}")
        print("Skills:", ",".join(c['skills']))
        print()

if __name__ == "__main__":

    run_career_prediction()