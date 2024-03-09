from near_seed_phrase.main import generate_seed_phrase, parse_seed_phrase



if __name__ == '__main__':
    # Generate a BIP39 seed phrase with its corresponding Keys
    # Returns:
    # {
    #     seed_phrase: str # BIP39 seed phrase
    #     secret_key: str # ed25519 secret/private key, formatted for NEAR (e.g. "ed25519:[SECRET_KEY]")
    #     public_key: str # ed25519 public key, formatted for NEAR (e.g. "ed25519:[PUBLIC_KEY]")
    #     public_key_hex: str # lowercase hex representation of public_key that can be used as an implicit account ID; see https://docs.near.org/integrator/implicit-accounts
    # } 
    key_info = generate_seed_phrase()
    print(key_info)

    # Recover keys from a BIP39 seed phrase (returns same response as generate_seed_phrase())
    key_confirm_info = parse_seed_phrase(key_info['seed_phrase'])
    print(key_confirm_info)