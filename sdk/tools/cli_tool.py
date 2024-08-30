import argparse
import json
from sdk.libraries.crypto_library import CryptoLibrary

class CliTool:
    def __init__(self):
        self.crypto_lib = CryptoLibrary()

    def generate_key_pair(self):
        # Generate a new RSA key pair
        key_pair = self.crypto_lib.generate_key_pair()
        private_key = key_pair.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key = key_pair.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )
        print(f"Private Key: {private_key.decode('utf-8')}")
        print(f"Public Key: {public_key.decode('utf-8')}")

    def sign_data(self, private_key, data):
        # Sign data using a private key
        signature = self.crypto_lib.sign_data(private_key, data.encode('utf-8'))
        print(f"Signature: {signature.hex()}")

    def verify_signature(self, public_key, data, signature):
        # Verify a signature using a public key
        verified = self.crypto_lib.verify_signature(public_key, data.encode('utf-8'), signature)
        print(f"Verified: {verified}")

    def encrypt_data(self, public_key, data):
        # Encrypt data using a public key
        cipher_text = self.crypto_lib.encrypt_data(public_key, data.encode('utf-8'))
        print(f"Cipher Text: {cipher_text.hex()}")

    def decrypt_data(self, private_key, cipher_text):
        # Decrypt data using a private key
        plain_text = self.crypto_lib.decrypt_data(private_key, cipher_text)
        print(f"Plain Text: {plain_text.decode('utf-8')}")

def main():
    parser = argparse.ArgumentParser(description="CLI Tool for SDK")
    subparsers = parser.add_subparsers(dest="command")

    generate_key_pair_parser = subparsers.add_parser("generate-key-pair", help="Generate a new RSA key pair")
    generate_key_pair_parser.set_defaults(func=generate_key_pair)

    sign_data_parser = subparsers.add_parser("sign-data", help="Sign data using a private key")
    sign_data_parser.add_argument("private_key", help="Private key")
    sign_data_parser.add_argument("data", help="Data to sign")
    sign_data_parser.set_defaults(func=sign_data)

    verify_signature_parser = subparsers.add_parser("verify-signature", help="Verify a signature using a public key")
    verify_signature_parser.add_argument("public_key", help="Public key")
    verify_signature_parser.add_argument("data", help="Data to verify")
    verify_signature_parser.add_argument("signature", help="Signature to verify")
    verify_signature_parser.set_defaults(func=verify_signature)

    encrypt_data_parser = subparsers.add_parser("encrypt-data", help="Encrypt data using a public key")
    encrypt_data_parser.add_argument("public_key", help="Public key")
    encrypt_data_parser.add_argument("data", help="Data to encrypt")
    encrypt_data_parser.set_defaults(func=encrypt_data)

    decrypt_data_parser = subparsers.add_parser("decrypt-data", help="Decrypt data using a private key")
    decrypt_data_parser.add_argument("private_key", help="Private key")
    decrypt_data_parser.add_argument("cipher_text", help="Cipher text to decrypt")
    decrypt_data_parser.set_defaults(func=decrypt_data)

    args = parser.parse_args()
    cli_tool = CliTool()
    args.func(cli_tool, args)

if __name__ == "__main__":
    main()
