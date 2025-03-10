from cryptography.fernet import Fernet

# Load the same encryption key (KEEP THIS SAFE!)
ENCRYPTION_KEY = b'3ZR6KFnAJSdUgfEgaTtd2RhpQumzMwLDjT4jaMd7Gjg='

cipher = Fernet(ENCRYPTION_KEY)

def decrypt_message(encrypted_message):
    """Decrypts an encrypted error message."""
    return cipher.decrypt(encrypted_message.encode()).decode()

def decrypt_log_file(file_path):
    """Reads and decrypts all encrypted errors from a log file."""
    with open(file_path, "r") as log_file:
        encrypted_errors = log_file.readlines()
    
    for i, encrypted_error in enumerate(encrypted_errors, start=1):
        try:
            decrypted_error = decrypt_message(encrypted_error.strip())
            print(f"\nDecrypted Error {i}:\n{decrypted_error}")
        except:
            print(f"Failed to decrypt error {i}. Possibly wrong key or corrupted data.")

# Decrypt all errors in the log file
decrypt_log_file("error_logs.txt")
