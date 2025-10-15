.PHONY: setup tracker peer1 peer2 distribute client reconstruct all clean

setup:
	pip3 install flask requests

tracker:
	@echo "Starting Tracker..."
	osascript -e 'tell application "Terminal" to do script "cd $(PWD) && python3 app.py"'

peer1:
	@echo "Starting Peer 1..."
	osascript -e 'tell application "Terminal" to do script "cd $(PWD) && python3 peer.py"'

peer2:
	@echo "Starting Peer 2..."
	osascript -e 'tell application "Terminal" to do script "cd $(PWD) && python3 peer2.py"'

distribute:
	@echo "Chunking and distributing file..."
	python3 distributor.py

client:
	@echo "Running client to download chunks..."
	python3 client_bob.py

reconstruct:
	@echo "Reconstructing final file from chunks..."
	python3 networks.py

all: setup tracker peer1 peer2
	@echo "Waiting for servers to spin up..."
	sleep 5
	make distribute
	make client
	make reconstruct

clean:
	@echo "Cleaning up downloaded and output files..."
	rm -f downloaded_chunk*.txt chunks/chunk_*.txt re.txt
