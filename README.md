# Challenge Lab 08 – Salted Hashes

## Overview

This project was completed for the Secure Communication and Cryptography module.

The aim of the lab was to recover plaintext passwords from six salted SHA-1 hashes provided in a database dump.

We used Python to identify the shared salt, perform a numeric brute-force attack, and carry out a dictionary attack using the `rockyou.txt` password wordlist.

We successfully recovered **4 out of 6 passwords (66.7%)**.

## Requirements

- Python 3
- `rockyou.txt` password wordlist
- Python's built-in `hashlib` library

No additional Python packages are required.

## Important – Download rockyou.txt Separately

**The `rockyou.txt` wordlist is not included in this repository and must be downloaded separately.**

You can obtain it from a trusted security wordlist collection, such as SecLists:

https://github.com/danielmiessler/SecLists

After downloading and extracting the wordlist:

1. Locate the `rockyou.txt` file.
2. Copy it into the same folder as the Python scripts.
3. Make sure the filename is exactly `rockyou.txt`.

The project folder should look like this:

```text
ChallengeLab08/
├── challenge_lab3.py
├── dict_crack.py
├── final_results.py
├── rockyou.txt
└── README.md
```

The dictionary attack will not run correctly without `rockyou.txt` in the expected location.

## Running the Programs

Open a terminal in the project folder.

### 1. Salt Verification and Numeric Brute Force

```bash
python challenge_lab3.py
```

This script tests candidate salts, identifies the correct salt and attempts to recover numeric passwords between 5 and 7 digits long.

### 2. Dictionary Attack

```bash
python dict_crack.py
```

This script reads passwords from `rockyou.txt`, combines each candidate with the recovered salt, hashes it using SHA-1 and compares the result against the remaining target hashes.

### 3. Final Results

```bash
python final_results.py
```

This script displays a summary of the recovered passwords and the unsuccessful attempts.

## Results

| Username | Recovered Password | Method |
|---|---|---|
| Sparky | Not recovered | Dictionary attack |
| Mark123 | Mark123 | Dictionary attack |
| superman | qwerty | Dictionary attack |
| security | 121298 | Numeric brute force |
| Tomtom | 54321 | Numeric brute force |
| JillC | Not recovered | Dictionary attack |

The dictionary attack tested approximately **14.3 million passwords in 9 seconds**.

The two remaining passwords were not recovered because none of the tested wordlist entries produced matching hashes.

## Security Observations

The experiment demonstrated how predictable passwords and reused salts can weaken password security.

SHA-1 is also unsuitable for modern password storage because it allows password guesses to be tested quickly. A dedicated password-hashing algorithm such as Argon2id, using a unique salt for each password, would provide stronger protection.

## Disclaimer

This project was completed for educational purposes using password hashes provided as part of a university cybersecurity challenge lab.
