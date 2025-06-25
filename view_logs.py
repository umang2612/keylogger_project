from cryptography.fernet import Fernet

# Load the saved key
with open("key.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Decrypt and print each line in the log
with open("keylogs.enc", "rb") as log_file:
    for line in log_file:
        try:
            decrypted = cipher.decrypt(line.strip())
            print(decrypted.decode())
        except Exception as e:
            print(f"Failed to decrypt a line: {e}")
