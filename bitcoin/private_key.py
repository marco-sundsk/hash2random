#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import base58
from typing import Union

"""
为了标识或者存储这个随机大整数, 可以用 256 比特位表示, 这 256 比特位可以编码为:
1. 16 进制形式;
2. Wallet Import Format (WIF);
3. WIF-compressed 形式.

随机生成一个32自己数据
$ openssl rand -hex 32              # 随机生成 32 字节随机数, 以 16 进制形式显示
d9815f47582f890ef4f818fd5dec98a6419fda23e57f1fed62ee0b9f79b1a785
$ openssl rand -hex 32              # 再测试一次
3bd5af025525af11f4471f299d600af51a6d697374b39ad19224a91b748a17ec

# 或者自己记一个数字, 12345678, 然后转成16进制即可
0000000000000000000000000000000000000000000000000000000000bc614e
"""


def scrub_input(hex_str_or_bytes: Union[str, bytes]) -> bytes:
    if isinstance(hex_str_or_bytes, str):
        hex_str_or_bytes = bytes.fromhex(hex_str_or_bytes)
    return hex_str_or_bytes


# wallet import format key - base58 encoded format
# https://bitcoin.stackexchange.com/questions/9244/private-key-to-wif
def gen_wif_key(private_key: Union[str, bytes], compressed_WIF: bool = False) -> bytes:
    private_key = scrub_input(private_key)

    # prepended mainnet version byte to private key
    mainnet_private_key = b'\x80' + private_key
    if compressed_WIF:
        mainnet_private_key = b'\x80' + private_key + b'\x01'
    # perform SHA-256 hash on the mainnet_private_key
    sha256 = hashlib.sha256()
    sha256.update(mainnet_private_key)
    hash = sha256.digest()

    # perform SHA-256 on the previous SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(hash)
    hash = sha256.digest()

    # create a checksum using the first 4 bytes of the previous SHA-256 hash
    # append the 4 checksum bytes to the mainnet_private_key
    checksum = hash[:4]

    hash = mainnet_private_key + checksum

    # convert mainnet_private_key + checksum into base58 encoded string
    return base58.b58encode(hash)


def decode_wif(wif: str) -> bytes:
    compressed = False
    if wif.startswith('K') or wif.startswith('L'):
        compressed = True
    decoded = base58.b58decode(wif)
    if compressed:
        private_key = decoded[1:-5]  # [80 xxx 1 checksum]
    else:
        private_key = decoded[1:-4]  # [80 xxx checksum]
    return private_key


if __name__ == '__main__':

    prikey = '0c28fca386c7a227600b2fe50b7cae11ec86d3bf1fbe471be89827e19d72aa1d'  # hex
    wif = gen_wif_key(prikey)
    print(wif)  # 5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ
    wif_compressed = gen_wif_key(prikey, True)
    print(wif_compressed)  # KwdMAjGmerYanjeui5SHS7JkmpZvVipYvB2LJGU1ZxJwYvP98617

    prikey = decode_wif('5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ')
    print(prikey.hex())  # 0c28fca386c7a227600b2fe50b7cae11ec86d3bf1fbe471be89827e19d72aa1d