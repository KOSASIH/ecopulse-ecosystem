import hashlib
import hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class CryptoLibrary:
    def __init__(self):
        self.backend = default_backend()

    def generate_key_pair(self):
        # Generate a new RSA key pair
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=self.backend
        )
        return key

    def sign_data(self, private_key, data):
        # Sign data using a private key
        signer = hmac.HMAC(private_key, hashlib.sha256, backend=self.backend)
        signer.update(data)
        return signer.finalize()

    def verify_signature(self, public_key, data, signature):
        # Verify a signature using a public key
        verifier = hmac.HMAC(public_key, hashlib.sha256, backend=self.backend)
        verifier.update(data)
        try:
            verifier.verify(signature)
            return True
        except ValueError:
            return False

    def encrypt_data(self, public_key, data):
        # Encrypt data using a public key
        cipher_text = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashlib.sha256()),
                algorithm=hashlib.sha256(),
                label=None
            )
        )
        return cipher_text

    def decrypt_data(self, private_key, cipher_text):
        # Decrypt data using a private key
        plain_text = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashlib.sha256()),
                algorithm=hashlib.sha256(),
                label=None
            )
        )
        return plain_text

# Example usage:
if __name__ == "__main__":
    crypto_lib = CryptoLibrary()
    key_pair = crypto_lib.generate_key_pair()
    private_key = key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    data = b"Hello, World!"
    signature = crypto_lib.sign_data(private_key, data)
    print(f"Signature: {signature.hex()}")

    verified = crypto_lib.verify_signature(public_key, data, signature)
    print(f"Verified: {verified}")

    cipher_text = crypto_lib.encrypt_data(public_key, data)
    print(f"Cipher Text: {cipher_text.hex()}")

    plain_text = crypto_lib.decrypt_data(private_key, cipher_text)
    print(f"Plain Text: {plain_text.decode('utf-8')}")
