from flask import Flask, request, jsonify

# Create a Flask app
app = Flask(__name__)

# This dictionary stores data in the format:
# { info_hash: { chunk_id: [ {peer_id, ip, port}, ...] } }
# It keeps track of which peer has which chunk of which file

peers_by_info_hash = {}

@app.route('/')
def home():
    # This is just a test route to check if the server is up
    return "Tracker is running!"

# This route allows Alice (or any peer) to register a chunk
@app.route('/register_chunk', methods=['POST'])
def register_chunk():
    # Get JSON data from the request body
    data = request.json

    # Extract required information
    info_hash = data.get("info_hash")
    chunk_id = str(data.get("chunk_id"))# Convert to string for consistent dict keys
    peer_id = data.get("peer_id")
    ip = data.get("ip")
    port = data.get("port")

    # Check if none of the fields are missing
    if not all([info_hash, chunk_id, peer_id, ip, port]):
        return jsonify({"error": "Missing parameters"}), 400

    # Initialize file structure if it doesn't exist
    if info_hash not in peers_by_info_hash:
        peers_by_info_hash[info_hash] = {}

    # Initialize chunk structure if it doesn't exist
    if chunk_id not in peers_by_info_hash[info_hash]:
        peers_by_info_hash[info_hash][chunk_id] = []

    # Create peer record
    peer = {"peer_id": peer_id, "ip": ip, "port": port}

    # Check if the peer is already registered
    if peer not in peers_by_info_hash[info_hash][chunk_id]:
        peers_by_info_hash[info_hash][chunk_id].append(peer)

    # Send success response
    return jsonify({"message": "Chunk registered successfully"}), 200

# This route allows Bob to ask which peers have chunks of a file
@app.route('/announce', methods=['GET'])
def announce():
    # Get the info_hash from the query parameters
    info_hash = request.args.get("info_hash")
    # If no info_hash is provided, return error
    if not info_hash:
        return jsonify({"error": "Missing info_hash"}), 400
    # If the file is not registered, return not found
    if info_hash not in peers_by_info_hash:
        return jsonify({"error": "File not found"}), 404

    return jsonify({
        "interval": 1800,
        "chunk_map": peers_by_info_hash[info_hash]
    })

def main():
    app.run(port=8080)
    
if __name__ == "__main__":
    main()

