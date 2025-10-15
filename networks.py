import os

def reconstructFile(storage: str, out: str) -> None:
    try:
        fileParts = []
        for fileName in os.listdir(storage):
            if fileName.startswith("downloaded_chunk_"):
                fileParts.append(fileName)

        # Sort: safe for names like downloaded_chunk_10.bin
        fileParts.sort(key=lambda name: int(name.split("_")[-1].split(".")[0]))
        print("📦 Files to reconstruct:", fileParts)

        total_bytes = 0
        with open(out, 'wb') as destination:
            for fileName in fileParts:
                filePath = os.path.join(storage, fileName)
                with open(filePath, 'rb') as partFile:
                    data = partFile.read()
                    destination.write(data)
                    print(f"📥 Appended {fileName}: {len(data)} bytes")
                    total_bytes += len(data)

        print(f"✅ File successfully reconstructed as '{out}' ({total_bytes} bytes).")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    reconstructFile("downloads", "re.txt")
