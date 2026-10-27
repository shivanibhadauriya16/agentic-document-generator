from dotenv import load_dotenv
from pathlib import Path
import os
from groq import Groq

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def writer_agent(topic, input_text):
    instruction_letter = f"""
    You are a professional writer and analyst.
    Create a clear, detailed, well-structured document about: {topic}.
    Use suitable headings and improve the document using any critic feedback
    included in the input.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": instruction_letter},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7,
        top_p=0.95
    )

    return response.choices[0].message.content