from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import MovneChatbot as Chatbot
import logging
import traceback
import os
from flask_cors import cross_origin
import socket
import psutil

# הגדרת הלוגר
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# הגדרת קידוד ברירת המחדל ל-UTF-8
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

# בדיקת מפתח ה-API
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error("OPENAI_API_KEY is not set in environment variables")
    raise ValueError("OPENAI_API_KEY is not set")
elif api_key == "sk-your-********here":
    logger.error("OPENAI_API_KEY is still set to default value")
    raise ValueError("Please set a valid OPENAI_API_KEY")

chatbot = Chatbot()

@app.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        logger.info(f"Received request: {request.json}")
        
        if not request.json:
            logger.error("No JSON data in request")
            return jsonify({"error": "No JSON data provided"}), 400, {'Content-Type': 'application/json; charset=utf-8'}
            
        query = request.json.get('query')
        user_id = request.json.get('user_id')
        
        if not query or not user_id:
            logger.error(f"Missing required fields: query={query}, user_id={user_id}")
            return jsonify({"error": "חסרים שדות חובה"}), 400, {'Content-Type': 'application/json; charset=utf-8'}
            
        logger.info(f"Processing query: {query} for user: {user_id}")
        
        response = chatbot.get_response(query)
        logger.info(f"Generated response: {response}")
        
        return jsonify({"response": response}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"שגיאה בעיבוד השאילתה: {str(e)}",
            "stack_trace": traceback.format_exc()
        }), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    try:
        return jsonify({"status": "ok", "message": "Flask server is running"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test-openai', methods=['GET'])
@cross_origin()
def test_openai():
    try:
        chatbot = Chatbot()
        # בדיקה פשוטה של החיבור ל-OpenAI
        response = chatbot.llm.predict("test")
        return jsonify({"status": "ok", "message": "OpenAI connection successful"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return False
        except socket.error:
            return True

def find_process_using_port(port):
    """מציאת תהליך שמשתמש בפורט מסוים"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return {
                        'pid': proc.pid,
                        'name': proc.name(),
                    }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

if __name__ == '__main__':
    logger.info("Starting Flask server...")
    
    # בדיקת פורט 5000
    if is_port_in_use(5000):
        process = find_process_using_port(5000)
        if process:
            logger.error(f"Port 5000 is already in use by process: {process}")
            logger.error("Please terminate the process and try again")
        else:
            logger.error("Port 5000 is already in use")
        exit(1)
    
    app.run(host='127.0.0.1', port=5000) 