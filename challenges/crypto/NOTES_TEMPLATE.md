# 🔐 Cryptography — Challenge Notes Template

## Challenge Info
- **Name:** 
- **Points:** 
- **Files:** 
- **Description:** 

---

## Step 1 — Identify the Cipher

### Quick Recognition Guide

| Pattern | Likely Encoding/Cipher |
|---------|------------------------|
| Ends in `=` or `==` | Base64 |
| Only `0-9 a-f` chars | Hex |
| Only `A-Z 2-7` + `=` | Base32 |
| Looks like shifted letters | Caesar / ROT-N |
| Dots and dashes | Morse code |
| `%XX` sequences | URL encoding |
| 4-char groups | Bacon cipher |
| Binary (`0` and `1` only) | Binary/ASCII |
| Very large numbers `(n, e, c)` | RSA |
| Repeating blocks | ECB mode AES |

---

## Step 2 — Solve

### Quick Decode Commands
```bash
# Base64
echo "BASE64STRING" | base64 -d

# Hex
echo "HEXSTRING" | xxd -r -p

# Python one-liner
python3 scripts/crypto_solver.py "YOUR_CIPHERTEXT"

# CyberChef Magic (online)
# https://gchq.github.io/CyberChef/#recipe=Magic(3,false,false,'')
```

### RSA Quick Checklist
```python
from Crypto.Util.number import long_to_bytes
import sympy

# Given: n, e, c
# Step 1: Factor n (try factordb.com first)
p, q = sympy.factorint(n).keys()

# Step 2: Compute private key
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

# Step 3: Decrypt
m = pow(c, d, n)
print(long_to_bytes(m))
```

### XOR Quick Solve
```python
# Single-byte XOR
ciphertext = bytes.fromhex("YOUR_HEX")
for key in range(256):
    result = bytes([b ^ key for b in ciphertext])
    if b'CTF' in result or b'flag' in result.lower():
        print(f"Key={key}: {result}")
```

### Hash Cracking
```bash
# MD5 / SHA1 — try online first
# https://crackstation.net

# hashcat
hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt   # MD5
hashcat -a 0 -m 100 hash.txt /usr/share/wordlists/rockyou.txt  # SHA1

# john
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

---

## Notes & Progress

```
[Cipher identified as] 

[Attempt 1] 
[Result]    

[Solution]  
```

---

## Flag
```
CTF{                                    }
```
