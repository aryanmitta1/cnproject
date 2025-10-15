#Import necessary modules
import requests
import os #for interacting with the file system
import time #for adding delays and tracking time
from file_chunking import chunk_file #function to split a file into chunks

#base url of the tracker server
TRACKER_URL = "http://127.0.0.1:8080"

# Function to wait until the tracker server is ready
def wait_for_tracker(url, timeout=5):
    print("Waiting for tracker to be ready...")
    start = time.time() #record the current time
    while True:
        try:
            #try sending a GET request to the tracker
            res = requests.get(url)
            if res.status_code == 200:
                print("Tracker is ready!") #Tracker is up and running
                return
        except:
            pass #ignore exceptions and try again
        
        #exit if the tracker doesn't respond within the timeout
        if time.time() - start > timeout:
            print("Tracker did not respond in time.")
            exit()
        time.sleep(0.5)  # Wait 0.5 seconds before retrying

#function distributing a file by chunking it and sending each chunk to a peer
def distribute(file_path):
    # splitting the file into chunks and get metadata
    metadata = chunk_file(file_path) #chunk the file using the imported chunk_file()
    chunks = metadata["chunks"]

    # list of peer servers (registered)
    peers = [
        {"peer_id": "peer1", "ip": "127.0.0.1", "port": 5001},
        {"peer_id": "peer2", "ip": "127.0.0.1", "port": 5002}
    ]

    #unique identifier for the file
    info_hash = "test123"  

#loop through each chunk and distribute it to a peer
    for chunk in chunks:
        i = chunk["index"] #chunk index number
        file_path = chunk["file"] #path to the chunk file
        
        #choosing a peer to send the chunk to (using round-robin method)
        peer = peers[i % len(peers)]
        peer_url = f"http://{peer['ip']}:{peer['port']}/receive_chunk"

        #opening and sending the chunk file to the peer via POST request
        with open(file_path, 'rb') as f:
            files = {'file': (f"chunk_{i}.bin", f)}
            r = requests.post(peer_url, files=files)
            print(f"Sent chunk_{i}.bin to {peer['peer_id']}")

        # register the chunk with the tracker
        register_data = {
            "info_hash": info_hash,
            "chunk_id": i,
            "peer_id": peer["peer_id"],
            "ip": peer["ip"],
            "port": peer["port"]
        }
        r = requests.post(f"{TRACKER_URL}/register_chunk", json=register_data)
        print(f"Registered chunk_{i}.bin to tracker")

#main program entry point
if __name__ == "__main__":
    #waiting until the tracker is online before continuing
    wait_for_tracker(f"{TRACKER_URL}/") 
    #distribute the file by calling distribute()
    distribute("test.txt") 
