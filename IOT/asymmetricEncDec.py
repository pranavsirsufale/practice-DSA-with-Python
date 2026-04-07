from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate keys
privateKey = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

publicKey = privateKey.public_key()

# message 
message = b"Hello Pran"

# Encrypt using Public Key
encrypted = publicKey.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message 'Hello Pran' after Encryption = ", encrypted)

# Decryption using Private Key
decrypted = privateKey.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print("Decrypted Message (actual plain text that was encrypted) = ", decrypted.decode())


# OUTPUT -> 



# Message 'Hello Pran' after Encryption =  b'\xdb\x17\xb8\x0f\xbe,\xbc\xf0\x92\xd5"\xf0\x0b=\xb35\xfa\xe9\xd8i\xb1\xe3\xde\xb1\xc7\x02s\xc0\x08\x1e\xb3\x82E\x9d\x84\xcbr\x05|H\xd6\x96\xa8O0\xe3fx\xdf(\x93<\x99\xaa\x1a\xc1\x1d\xc6$M\xea\x95\n\xe0f\x88\xeb(\xc8\x10\xa6\xfd\xfc\x8f}\x91=#r\x99\xcb\xc0\xaf\x88\x9c\xa6\xc9\xa8@|\x1e\xcf\x19\t\xbdL\x06J+\x00\xb8Kh\x00\xfd\xda\xd7\xeb\x18L\xa7\xfe+G\xac?\x82&2\xd9N\xb3\x84\xe5\xd7\xe4\xe1\xc9\x17\xa9\x98.E\x98tXn\x8c\x18A\x82,UA(\xe6N\x03p\xc2\xe4\xe04\x89/\xe50\xa5\xe4ln\x940D\xe5[k\xae\xb8\xecv(^\xf3\xbaU\xf8\n\x98\xd11Q\xe3m\xd7\x10\xef$\xf75q\x0cXx)\x833\xc3\xdd\xda\xee\xa2\xd7\xb4\xb2d\x0c\xec\xacg\xef\xab:( \xa4\x04C\xedxd\xb0r\xee\x7fmRBi\x8d\xde\x05\x9c\x80#.\x08\xf4\xd7\x8aCB\x0c\xdc\x08\xc7\xf2\x83`\r^\xa5\x9dtmi'
# Decrypted Message (actual plain text that was encrypted) =  Hello Pran