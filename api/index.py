from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def generate():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    negocio = data.get('negocio', 'barberia')
    prompt_texto = f"Genera 3 hooks virales para {negocio}"

    # 1. Generar texto
    text_resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt_texto}]
    )
    texto = text_resp.choices[0].message.content

    # 2. Generar imagen
    image_resp = client.images.generate(
        model="dall-e-3",
        prompt=f"Flyer profesional para {negocio}, estilo moderno, promocion atractiva, alta calidad, 4k",
        size="1024x1024",
        n=1
    )
    imagen_url = image_resp.data[0].url

    return jsonify({
        "texto": texto,
        "imagen": imagen_url
    })

if __name__ == '__main__':
    app.run()
