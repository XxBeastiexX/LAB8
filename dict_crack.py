"""Dictionary attack on the four alphanumeric Lab 08 SHA-1 hashes."""
import hashlib
import sys
import time
from pathlib import Path

SALT = 'www.exploringsecurity.com'
TARGET_HASHES = [
    '2834da08d58330d8dafbb2ac1c0f85f6b3b135ef',
    '92e54f10103a3c511853c7098c04141f114719c1',
    '437fbc6892b38db6ac5bdbe2eab3f7bc924527d9',
    'f44f3b09df53c1c11273def13cacd8922a86d48c',
]


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else 'rockyou.txt')
    print(f'[*] Wordlist: {path.resolve()}')
    if not path.is_file():
        print(f'[-] File not found: {path}')
        print('    Put rockyou.txt in the current folder or supply its path.')
        return

    results = dict.fromkeys(TARGET_HASHES)
    remaining = len(results)
    tried = 0
    start = time.perf_counter()
    salt_bytes = SALT.encode('utf-8')

    # ISO-8859-1 mirrors the Java reader; UTF-8 mirrors its hashing step.
    with path.open('r', encoding='iso-8859-1') as wordlist:
        for line in wordlist:
            if remaining == 0:
                break
            word = line.rstrip('\r\n')
            digest = hashlib.sha1(salt_bytes + word.encode('utf-8')).hexdigest()
            if digest in results and results[digest] is None:
                results[digest] = word
                remaining -= 1
                print(f'\n[+] CRACKED {digest} -> {word}', flush=True)
            tried += 1
            if tried % 1_000_000 == 0:
                print(f'[*] Tried {tried:,} words; {remaining} hashes left', flush=True)

    print(f'\n[=] Done in {time.perf_counter()-start:.1f}s; tried {tried:,} words')
    for digest, password in results.items():
        print(f'    {digest} -> {password if password is not None else "(not found)"}')


if __name__ == '__main__':
    main()
