from flask import Flask, request, send_file
import os

app = Flask(__name__)
CHUNK_DIR = "chunks"

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    print(f"📩 Notified for chunk {data['chunk_id']}")
    return "OK", 200

@app.route('/receive_chunk', methods=['POST'])
def receive_chunk():
    chunk = request.files['file']
    filename = chunk.filename
    os.makedirs(CHUNK_DIR, exist_ok=True)
    filepath = os.path.join(CHUNK_DIR, filename)
    chunk.save(filepath)
    print(f"📥 Received chunk: {filename}, saved to {filepath}")
    return "Chunk received", 200

@app.route('/get_chunk', methods=['GET'])
def get_chunk():
    filename = request.args.get("name")
    filepath = os.path.join(CHUNK_DIR, filename)
    if os.path.exists(filepath):
        print(f"📤 Sending chunk: {filename}")
        return send_file(filepath)
    else:
        print(f"❌ Chunk not found: {filename}")
        return "Chunk not found", 404

if __name__ == '__main__':
    app.run(port=5002)
