#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Marco'

"""

"""

import math
# the blockhash that used as random source
hashes = [
    '0x9934b223bb335fd8ae4d22cb36d1038305effe8a9e2325ca3790f76fca4e7435',  # 922508
    '0x40a63c25fef700beb1fd925acc4578d0241d9f0f121c93e0e27767358b23ea0e',  # 922509
    '0xa20f7f54b64c34c2e2971b2b706f5d8fbb5721b15fd8a3fa8f4fee1890623ef0',  # 922510
    '0x6fcf87293babf5e82099f9bca59804027a90b2f49355753d7fc9fc4d97bc4e91',  # 922511
]
# the scope of participant
scope = 10716

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

