from cryptography.fernet import Fernet

#Generate key
key = Fernet.generate_key()
print("Generated key via 'Fernet',", key)
cipher = Fernet(key)
print("cipher of generated key: ", cipher)

#Encryption
message = "Hello pran".encode()
encrypted = cipher.encrypt(message)
print("Encrypted 'Hello pran':", encrypted)

# Decrypt
decrypted = cipher.decrypt(encrypted)
print("Decrepted message.:", decrypted)
print("Decrypted message in string after decode:", decrypted.decode())


# OUTPUT 

# Generated key via 'Fernet', b'2hbPJ0PbPW4wh8Uz3KrDQmQZOfiemMjX42KweYpgwUs='
# cipher of generated key:  <cryptography.fernet.Fernet object at 0x750206d02690>
# Encrypted 'Hello pran': b'gAAAAABp1PziYs3G3zPIl4Eqe2C_LHt0431paqE1R_W74rSVY8Vp6xnt2R9G57A13R9zzcpMNO1JS6wQ_fzPTDDrzrbixHrj_Q=='
# Decrepted message.: b'Hello pran'
# Decrypted message in string after decode: Hello pran