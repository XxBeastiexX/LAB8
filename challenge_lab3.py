"""Recover the shared salt and numeric passwords for Lab 08."""
import hashlib
import re
import sys
import time
from pathlib import Path

DIGIT_HASHES = {
    'fafa4483874ec051989d53e1e432ba3a6c6b9143',
    '06f6fe0f73c6e197ee43eff4e5f7d10fb9e438b2',
}
ALPHANUM_HASHES = [
    '2834da08d58330d8dafbb2ac1c0f85f6b3b135ef',
    '92e54f10103a3c511853c7098c04141f114719c1',
    '437fbc6892b38db6ac5bdbe2eab3f7bc924527d9',
    'f44f3b09df53c1c11273def13cacd8922a86d48c',
]

# The original Java program placed these candidates first, then scanned the lab text.
PRIORITY_CANDIDATES = [
    'www.exploringsecurity.com', 'exploringsecurity.com',
    'exploringsecurity', 'CommonHash',
]


def candidates_from_text(text):
    candidates = dict.fromkeys(PRIORITY_CANDIDATES)
    for token in text.split():
        token = re.sub(r'''^[.,:;()\[\]{}"']+|[.,:;()\[\]{}"']+$''', '', token).strip()
        if token:
            candidates[token] = None
            candidates[token.lower()] = None
    return list(candidates)


def sha1_hex(salt, password, order):
    data = (salt + password if order == 'salt+pass' else password + salt)
    return hashlib.sha1(data.encode('utf-8')).hexdigest()


def numeric_passwords():
    for length in (5, 6, 7):
        for number in range(10 ** length):
            yield f'{number:0{length}d}'


def find_salt(candidates):
    start = time.perf_counter()
    for index, salt in enumerate(candidates, 1):
        print(f'[*] Checking candidate {index}/{len(candidates)}: {salt!r}', flush=True)
        for order in ('salt+pass', 'pass+salt'):
            for password in numeric_passwords():
                digest = sha1_hex(salt, password, order)
                if digest in DIGIT_HASHES:
                    print(f'\n[+] Salt found in {time.perf_counter()-start:.1f} seconds')
                    print(f'[+] Salt: {salt}')
                    print(f'[+] Order: {order}')
                    print(f'[+] Password: {password}')
                    print(f'[+] Hash: {digest}')
                    return salt, order
    return None


def crack_digits(salt, order):
    remaining = set(DIGIT_HASHES)
    print('\n--- Numeric password results ---')
    for password in numeric_passwords():
        digest = sha1_hex(salt, password, order)
        if digest in remaining:
            print(f'[+] {digest} -> {password}')
            remaining.remove(digest)
            if not remaining:
                break
    for digest in remaining:
        print(f'[-] {digest} -> (not found)')


def main():
    # Optional: pass a UTF-8 text file containing the lab handout text.
    text = Path(sys.argv[1]).read_text(encoding='utf-8') if len(sys.argv) > 1 else ''
    candidates = candidates_from_text(text)
    print(f'[*] Checking {len(candidates)} possible salts')
    result = find_salt(candidates)
    if result is None:
        print('[-] No salt found. Supply more candidate text from the lab handout.')
        return
    salt, order = result
    crack_digits(salt, order)
    print('\n--- Alphanumeric hashes for dictionary attack ---')
    for digest in ALPHANUM_HASHES:
        print(digest)
    print('\nNext: run dict_crack.py with your wordlist.')


if __name__ == '__main__':
    main()
