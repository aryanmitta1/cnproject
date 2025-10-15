import requests
import os

TRACKER_URL = "http://127.0.0.1:8080"
INFO_HASH = "test123"

def download_chunk(peer, chunk_id):
    url = f"http://{peer['ip']}:{peer['port']}/get_chunk"
    params = {"name": f"chunk_{chunk_id}.bin"}
    folder = "downloads"
    os.makedirs(folder, exist_ok=True) 

    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            filename = os.path.join(folder, f"downloaded_chunk_{chunk_id}.bin")
            with open(filename, "wb") as f:
                f.write(res.content)
            print(f"[+] Downloaded chunk {chunk_id} from {peer['peer_id']}")
        else:
            print(f"[!] Failed to get chunk {chunk_id} from {peer['peer_id']}")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    res = requests.get(f"{TRACKER_URL}/announce", params={"info_hash": INFO_HASH})
    data = res.json()
    chunk_map = data["chunk_map"]

    for chunk_id, peers in chunk_map.items():
        download_chunk(peers[0], chunk_id)
