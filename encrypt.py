from cryptography.fernet import Fernet

# generate a key to use for encryption
key = Fernet.generate_key()
print(key)

# create a Fernet object with the key
fernet = Fernet(key)

# encrypt the password and write it to a file
encrypted_password = fernet.encrypt(b"yourpassword")
with open("password.txt", "wb") as f:
    f.write(encrypted_password)