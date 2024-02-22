from bitcoinutils.setup import setup
from bitcoinutils.script import Script
from bitcoinutils.keys import P2wshAddress, PrivateKey



def main():
    # always remember to setup the network
    setup('testnet')

    #
    # P2WSH
    #
    p2wpkh_key = PrivateKey.from_wif('cNn8itYxAng4xR4eMtrPsrPpDpTdVNuw7Jb6kfhFYZ8DLSZBCg37')
    script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
    p2wsh_addr = P2wshAddress.from_script(script)
    print("P2WSH of P2PK:", p2wsh_addr.to_string() )


if __name__ == "__main__":
    main() # tb1qy4kdfavhluvnhpwcqmqrd8x0ge2ynnsl7mv2mdmdskx4g3fc6ckq8f44jg