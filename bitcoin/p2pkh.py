#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import base58

"""
    P2PKH(Pay-to-Public-Key-Hash)
        是最原始的地址,由公钥通过 Hash 计算后得到，它们都以 1 开头.

    我们以前面介绍过的 Compressed 公钥(03f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a)为例,介绍一下从公钥转换得到地址的步骤：
    1. 计算其 SHA256
    2. 对上面结果计算 RIPEMD-160 哈希
    3. 计算 checksum,规则是对上面结果前面加上版本号(主网为 0x00,测试网为 0x6f),然后计算两次 SHA256
    4. 用格式 [version][ripemd160_hash][checksum] 构造出结果
    5. 对上面结果进行 Base58Check 编码

    用 Compressed 公钥计算出来的,被称为“Compressed 地址”;
    如果用 Uncompressed 公钥重复进行上面过程,则会得到另外一个地址,称为“Uncompressed 地址”.
    一个比特币私钥对应两个地址(Compressed/Uncompressed 地址),它们都是合法的.


"""
def sha256(inputs: bytes) -> bytes:
    """ Computes sha256 """
    sha = hashlib.sha256()
    sha.update(inputs)
    return sha.digest()


def ripemd160(inputs: bytes) -> bytes:
    """ Computes ripemd160 """
    rip = hashlib.new('ripemd160')
    rip.update(inputs)
    return rip.digest()


def base58_cksum(inputs: bytes) -> bytes:
    """ Computes base 58 four bytes check sum """
    s1 = sha256(inputs)
    s2 = sha256(s1)
    checksum = s2[0:4]
    return checksum


def pubkey_compressed_to_uncompressed(compressed_pubkey: bytes) -> bytes:
    """ Converts compressed pubkey to uncompressed format """
    assert len(compressed_pubkey) == 33
    # modulo p which is defined by secp256k1's spec
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    x = int.from_bytes(compressed_pubkey[1:33], byteorder='big')
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p + 1) // 4, p)
    if compressed_pubkey[0] % 2 != y % 2:
        y = p - y
    y_bytes = y.to_bytes(32, byteorder='big')
    return b'\04' + compressed_pubkey[1:33] + y_bytes  # x + y


def pubkey_to_p2pkh_addr(pubkey: bytes, version: bytes) -> bytes:
    """ Derives legacy (p2pkh) address from pubkey """
    out1 = sha256(pubkey)
    out2 = ripemd160(out1)
    # Base-58 encoding with a checksum
    checksum = base58_cksum(version + out2)
    address = base58.b58encode(version + out2 + checksum)
    return address


if __name__ == '__main__':

    pubkey = '03f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a'

    pubkey_uncompressed = b''
    pubkey_compressed = b''

    if pubkey.startswith('04'):  # uncompressed
        pubkey_uncompressed = bytes.fromhex(pubkey)
        if ord(bytearray.fromhex(pubkey[-2:])) % 2 == 0:
            pubkey_compressed_hex_str = '02' + pubkey[2:66]
        else:
            pubkey_compressed_hex_str = '03' + pubkey[2:66]
        pubkey_compressed = bytes.fromhex(pubkey_compressed_hex_str)
    else:  # compressed
        pubkey_uncompressed = pubkey_compressed_to_uncompressed(bytes.fromhex(pubkey))
        pubkey_compressed = bytes.fromhex(pubkey)

    print("compressed public key =", pubkey_compressed.hex())
    print("uncompressed public key =", pubkey_uncompressed.hex())
    main_version = b'\x00'  # 0x00 for mainnet, 
    test_version = b'\x6f'  # 0x6f for testnet

    addr_compressed = pubkey_to_p2pkh_addr(pubkey_compressed, main_version)
    addr_uncompressed = pubkey_to_p2pkh_addr(pubkey_uncompressed, main_version)

    test_addr_compressed = pubkey_to_p2pkh_addr(pubkey_compressed, test_version)
    test_addr_uncompressed = pubkey_to_p2pkh_addr(pubkey_uncompressed, test_version)
    print("mainnet address (uncompressed) = ", addr_uncompressed)  # 1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x
    print("mainnet address (compressed) = ", addr_compressed)  # 1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy

    print("testnet address (uncompressed) = ", test_addr_compressed)  # mxdivjAqQSQj4LrAMX1XLQidyfU3pCWeS7
    print("testnet address (compressed) = ", test_addr_uncompressed)  # miY1V5L3QDaZVjrMT2Sw2WhHn63GzsNFQB