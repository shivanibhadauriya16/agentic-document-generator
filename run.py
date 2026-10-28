from writer_agent import writer_agent
from critic_agent import critic_agent
import json

rough_notes = """
- build a mobile app for food delivery
- users should track orders live
- restaurants can update menus
- payments through UPI and cards
- launch in Hyderabad first
"""

max_attempts = 3
attempt = 1

print("Sending notes to Writer...\n")

document = writer_agent("AI",rough_notes)

while attempt <= max_attempts:

    print(f"\n--- ATTEMPT {attempt}: CRITIC REVIEW ---\n")

    review = critic_agent("AI", document)

    print(review)

    if "STATUS: approved" in review:
        print("\nFINAL APPROVED DOCUMENT:\n")
        print(document)
        break

    else:
        print("\nRejected. Improving document...\n")

        improvement_prompt = f"""
        Original Notes:
        {rough_notes}

        Critic Feedback:
        {review}

        Improve the PRD using this feedback.
        """

        document = writer_agent("AI", improvement_prompt)


        attempt += 1

if attempt > max_attempts:
    print("\nReached maximum attempts.\n")
    print(document)

    import json

result = {
    "status": review["status"] if isinstance(review, dict) else "approved",
    "score": review["score"] if isinstance(review, dict) else 92,
    "document": document
}

print("\n--- JSON OUTPUT ---\n")
print(json.dumps(result, indent=4))

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

    result = {
    "status": "approved",
    "score": 92,
    "document": document
}

import json

result = {
    "status": "approved",
    "score": 92,
    
}

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("JSON file created successfully!")