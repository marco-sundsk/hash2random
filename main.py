#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Marco'

"""

"""

import math
# the blockhash that used as random source
hashes = [
    '0x8cc2b24c321aec063c8cea612205b1d6f29c05b1e57c3e0ee89a6e098bd24c5c',  # 1522171
    '0xa8db223ec557970a1c6c1703f7389aa90dd70aa1248117dbcaacd75bb39c4db9',  # 
    '0x09ca97024e075e31b1b99a1e89e377dad3decd6f5656e165cd97bdee100f5ca8',  # 
    '0x8167be1fe2f52d9dae695bfa1fdd83d7886f2fdffd2857f78587cfa543cd19ee',  # 

    '0xfa8fe621be2be23c28026c63a68ed94d380bf3e986883ff7bea25dc6c9ebd900',  # 
    '0x434b23d9bb651f249236418133081d67de47055b8efa8fe7836c5e29caebd6fa',  # 
    '0x4aea47d545eeb1d63876b538e446dc9ff61b878c96c78029c2f9fec4f13667d0',  # 1522177
]
# the scope of participant
scope = 12474

random_seq = []
rslt_seq = []


def fillin_randomsource(hash, pace):
    if hash.startswith('0x'):
        hash = hash[2:]
    print('Fill in random source:', hash)

    for i in range(0, len(hash), pace):
        hex_str = hash[i:i+pace]
        # print(hex_str)
        random_seq.append(int(hex_str, 16))


if __name__ == '__main__':

    print('Blockhash random Tool, scope is ', scope)

    if scope < 256:
        pace = 2
    elif scope < 65536:
        pace = 4
    else:
        pace = 8

    for hash in hashes:
        fillin_randomsource(hash, pace)

    
    print('We got %s random seeds' % len(random_seq))

    for random in random_seq:
        rank = math.floor(scope * random / 16**pace) + 1
        if rank not in rslt_seq:
            rslt_seq.append(rank)
        else:
            # print('%s already in rank sequence' % rank)
            pass

    print('result len:', len(rslt_seq))
    print(rslt_seq)
    print('End.')

