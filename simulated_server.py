import socket

HOST = '127.0.0.1'
PORT = 9001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print("🛰️ Simulated server listening...")
    conn, addr = server.accept()
    with conn:
        print(f"📥 Connection from {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("🔐 Encrypted log received:", data.decode())
