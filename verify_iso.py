import os
import hashlib

p = "LMG-OS-1.0.0-amd64.iso"
if os.path.exists(p):
    sz = os.path.getsize(p)
    print(f"ISO File: {p}")
    print(f"ISO Size: {sz} bytes ({sz / (1024*1024):.2f} MB)")
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    sha = h.hexdigest()
    print(f"SHA256: {sha}")
    with open("ISO_VERIFICATION.txt", "w") as out:
        out.write(f"ISO File: {p}\nISO Size: {sz} bytes ({sz / (1024*1024):.2f} MB)\nSHA256: {sha}\n")
else:
    print("ISO File NOT found!")
