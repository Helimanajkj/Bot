
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return "Bot is alive!"

@socketio.on('connect', namespace='/ws')
def handle_connect():
    print('Client connected')

def keep_alive():
    """Start the Flask server in a separate thread to keep the bot alive"""
    def run():
        socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, log_output=False, allow_unsafe_werkzeug=True)
    
    server_thread = threading.Thread(target=run)
    server_thread.daemon = True
    server_thread.start()
    print("🌐 Keep-alive server started on port 5000")

if __name__ == '__main__':
    keep_alive()
