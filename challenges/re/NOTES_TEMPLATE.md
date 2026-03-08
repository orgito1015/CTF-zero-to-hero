# 🔍 Reverse Engineering — Challenge Notes Template

## Challenge Info
- **Name:** 
- **Points:** 
- **Binary:** 
- **Description:** 

---

## Step 1 — Quick Triage

```bash
file ./binary
strings ./binary | grep -iE "flag|ctf|password|key|correct|wrong"
ltrace ./binary          # trace library calls
strace ./binary          # trace syscalls
./binary                 # just run it — what does it do?
```

---

## Step 2 — Static Analysis (Ghidra)

1. Open Ghidra → New Project → Import file
2. Double-click → Analyze (accept defaults)
3. **Symbol Tree** → `Functions` → find `main`
4. Look for:
   - `strcmp` / `strncmp` — string comparisons
   - `scanf` / `fgets` — input functions
   - Functions named `check`, `validate`, `win`, `correct`
5. Decompiler window shows C-like pseudocode

### Common Patterns
```c
// Pattern 1: Direct string compare
if (strcmp(input, "secret_key") == 0) { print_flag(); }

// Pattern 2: XOR encoding
for (i=0; i < len; i++) { expected[i] = input[i] ^ 0x42; }

// Pattern 3: Math check
if (input * 1337 == 0xDEADBEEF) { print_flag(); }
```

---

## Step 3 — Dynamic Analysis (GDB)

```bash
gdb ./binary

# Inside GDB (pwndbg recommended)
info functions          # list all functions
disassemble main        # show assembly of main
b *main+50              # set breakpoint at offset
b strcmp                # break at strcmp
run                     # start
n                       # next instruction
x/s $rdi               # examine string at register rdi (first arg)
x/s $rsi               # examine string at rsi (second arg — the expected value!)
```

### Bypass strcmp with GDB
```bash
# Set breakpoint right before strcmp
b strcmp
run
# When it hits strcmp, both args are in rdi (input) and rsi (expected)
x/s $rdi    # your input
x/s $rsi    # ← this is the correct password!
```

---

## Step 4 — Patching (if needed)

```bash
# Find the jump instruction address in Ghidra
# Then patch with radare2
r2 -w ./binary
[0x00000000]> s 0xADDRESS
[0x0000ADDR]> wa jmp 0xTARGET   # patch jump
[0x0000ADDR]> q
```

---

## Notes & Progress

```
[Key functions found] 

[Algorithm]          

[Attempt 1]          
[Result]             

[Solution]           
```

---

## Flag
```
CTF{                                    }
```
