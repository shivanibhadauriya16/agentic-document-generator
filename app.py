from flask import Flask, request, jsonify, render_template
from writer_agent import writer_agent
from critic_agent import critic_agent
import os
import threading
import time
import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ping')
def ping():
    return jsonify({"status": "alive"})

def ping_server():
    """Background task to ping the server every 14 minutes to prevent Render cold starts."""
    url = os.environ.get('RENDER_EXTERNAL_URL')
    if not url:
        url = 'http://localhost:5000'
        
    ping_url = url.rstrip('/') + '/api/ping'
    while True:
        time.sleep(14 * 60) # Wait 14 minutes
        try:
            urllib.request.urlopen(ping_url)
            print(f"Pinged {ping_url} to keep server alive.")
        except Exception as e:
            print(f"Failed to ping {ping_url}: {e}")

# Start the background thread
threading.Thread(target=ping_server, daemon=True).start()

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic', 'General')
    notes = data.get('notes', '')
    max_attempts = int(data.get('max_attempts', 3))
    
    attempt = 1
    attempts_history = []
    
    current_input = f"Original Notes:\n{notes}"
    document = writer_agent(topic, current_input)
    
    while attempt <= max_attempts:
        review = critic_agent(topic, document)
        
        history_item = {
            "attempt": attempt,
            "document": document,
            "review": review
        }
        attempts_history.append(history_item)
        
        if "STATUS: approved" in review.lower() or "status: approved" in review.lower() or "status: approved" in review:
            break
            
        if attempt < max_attempts:
            improvement_prompt = f"""
            Topic: {topic}
            
            Original Notes:
            {notes}
            
            Critic Feedback:
            {review}
            
            Improve the document using this feedback. Ensure all previous constraints are met.
            """
            document = writer_agent(topic, improvement_prompt)
            
        attempt += 1
        
    return jsonify({
        "success": True,
        "attempts": attempts_history,
        "final_document": document
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
