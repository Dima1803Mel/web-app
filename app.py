from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'version': os.environ.get('APP_VERSION', 'unknown'),
        'host': socket.gethostname(),
        'message': 'Updated via CI/CD!' # Новое поле
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)