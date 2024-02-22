import base58
import binascii
from near_api import signer
from nacl import signing, encoding

def get_implicit_account_id_from_pk(pk: bytes) -> bytes:
    account_id = binascii.hexlify(base58.b58decode(pk))
    return account_id

if __name__ == '__main__':
    pk_in_b58 = "BGCCDDHfysuuVnaNVtEhhqeT4k9Muyem3Kpgq2U1m9HX"
    hex = binascii.hexlify(base58.b58decode(pk_in_b58))
    print('implicit account ID:', hex)
    print(get_implicit_account_id_from_pk(pk_in_b58))

    sk = signing.SigningKey.generate()
    pk = sk.verify_key.encode()
    print("sk in base58:", base58.b58encode(pk).decode('utf-8'))
    print("PK in base58:", base58.b58encode(sk.encode()).decode('utf-8'))
    print("implicit AID:", pk.hex())

    # random_key = signer.KeyPair(False)
    # print("b58 encoded PK:", random_key.encoded_public_key())
    # print("b58 encoded sk:", random_key.encoded_secret_key())
    # print("corresponding implicit accountID:", get_implicit_account_id_from_pk(random_key.encoded_public_key()))


