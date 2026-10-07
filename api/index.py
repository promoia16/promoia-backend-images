from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return 'PromoIA Backend Activo!'

@app.route('/api/generate', methods=['POST', 'GET', 'OPTIONS'])
def generate():
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({'status': 'ok'})
    try:
        data = request.get_json() or {}
        prompt = data.get('prompt', 'anuncio viral para barberia moderna')
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        r = client.images.generate(model="dall-e-3", prompt=prompt, size="1024x1024", n=1)
        return jsonify({'image_url': r.data[0].url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
