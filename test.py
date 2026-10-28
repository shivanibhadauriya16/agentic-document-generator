from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    print("AI:", chat_completion.choices[0].message.content)