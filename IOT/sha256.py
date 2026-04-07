import hashlib

data = "Hello, World!"
dataByte = data.encode('utf-8')
print("Data Byte:", dataByte)

# create sha-256 hash object
hashObj = hashlib.sha256(dataByte)
print("Hash Object:", hashObj)

# Hexadecimal digest
hashHex = hashObj.hexdigest()
print("SHA-256 Hash hex:", hashHex)

# OUTPUT :

#       Data Byte: b'Hello, World!'
#       Hash Object: <sha256 _hashlib.HASH object @ 0x7b9df571bf10>
#       SHA-256 Hash hex: dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f