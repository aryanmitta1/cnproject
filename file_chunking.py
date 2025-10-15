import os
import hashlib

def chunk_file(file_path, chunk_size=1024):
    """
    Splits a file into chunks and writes each chunk to a separate file.
    
    Args:
        file_path (str): Path to the file to be chunked.
        chunk_size (int): Size of each chunk in bytes (default is 1 MB).
    
    Returns:
        dict: Metadata about the chunked file including chunk file names, hashes, and sizes.
    """
    # Create an output directory for the chunks in the same directory as the file.
    output_dir = os.path.join(os.path.dirname(file_path), "chunks")
    os.makedirs(output_dir, exist_ok=True)
    
    metadata = {
        "file_name": os.path.basename(file_path),
        "file_size": os.path.getsize(file_path),
        "chunk_size": chunk_size,
        "num_chunks": 0,
        "chunks": []  # List to store details for each chunk.
    }
    
    with open(file_path, "rb") as f:
        index = 0
        while True:
            # Read a block of data of size 'chunk_size'
            chunk = f.read(chunk_size)
            if not chunk:
                break  # End of file reached.
            
            # Compute the SHA-256 hash for the current chunk.
            chunk_hash = hashlib.sha256(chunk).hexdigest()
            
            # Create a filename for the chunk (e.g., chunk_0.bin, chunk_1.bin, etc.)
            chunk_file_name = os.path.join(output_dir, f"chunk_{index}.bin")
            with open(chunk_file_name, "wb") as cf:
                cf.write(chunk)
            
            # Store metadata for this chunk.
            metadata["chunks"].append({
                "index": index,
                "file": chunk_file_name,
                "hash": chunk_hash,
                "size": len(chunk)
            })
            index += 1
            
    metadata["num_chunks"] = index
    return metadata

if __name__ == "__main__":
    # Construct the file path to "test.txt" on the Desktop.
    # This works on Unix-like systems (macOS, Linux). For Windows, update the path accordingly.
    file_to_chunk = os.path.expanduser("~/Desktop/test.txt")
    
    meta = chunk_file(file_to_chunk)
    
    print("File chunking complete. Metadata:")
    print(f"Original File: {meta['file_name']}")
    print(f"File Size: {meta['file_size']} bytes")
    print(f"Chunk Size: {meta['chunk_size']} bytes")
    print(f"Number of Chunks: {meta['num_chunks']}")
    for chunk in meta["chunks"]:
        print(f"Chunk {chunk['index']}: {chunk['file']} (Size: {chunk['size']} bytes, SHA-256: {chunk['hash']})")
