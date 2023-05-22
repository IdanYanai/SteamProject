from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


class Encryptor(object):
    def __init__(self, PKey=None):
        if PKey:
            self.PKey = PKey
        else:
            self.SKey = RSA.generate(1024)
            self.PKey = self.SKey.publickey()
            print("Public key: (n=%s, e=%s)" % ({hex(self.PKey.n)}, {hex(self.PKey.e)}))
            print("Secret key: (n=%s, d=%s)" % ({hex(self.PKey.n)}, {hex(self.SKey.d)}))

    def rsa_encrypt(self, msg):
        encryptor = PKCS1_OAEP.new(self.PKey)
        encrypted = encryptor.encrypt(msg.encode())
        return base64.b64encode(encrypted)

    def rsa_decrypt(self, msg):
        msg = base64.b64decode(msg)
        decryptor = PKCS1_OAEP.new(self.SKey)
        decrypted = decryptor.decrypt(msg)
        return decrypted.decode()


# Pog = Encryptor()
# password = "123456789"
# e = Pog.rsa_encrypt(password)
# print(e)
# d = Pog.rsa_decrypt(e)
# print(d)
