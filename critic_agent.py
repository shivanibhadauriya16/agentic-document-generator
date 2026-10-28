from dotenv import load_dotenv
from pathlib import Path
import os
from groq import Groq

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def critic_agent(topic, document):
    instruction_letter = f"""
You are a strict senior reviewer and editor.

Evaluate the following document about '{topic}' carefully based on:

1. Completeness
2. Clarity
3. Depth of knowledge
4. Realism
5. Structure
6. Relevance to the topic

Scoring Rules:
- 90-100 = excellent
- 75-89 = good but improvable
- 50-74 = weak
- below 50 = poor

Reject if:
- key aspects of the topic are missing
- explanations are vague
- arguments or details are weak
- the structure is poor

Respond EXACTLY in this format:

STATUS: approved OR rejected
SCORE: number out of 100
MISSING: missing aspects or none
FEEDBACK: detailed improvement feedback
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": instruction_letter},
            {"role": "user", "content": document}
        ]
    )

    return response.choices[0].message.content