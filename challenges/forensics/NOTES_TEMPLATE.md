# 🕵️ Forensics / OSINT — Challenge Notes Template

## Challenge Info
- **Name:** 
- **Points:** 
- **Files:** 
- **Description:** 

---

## Step 1 — Identify & Triage

```bash
# Always run these first
python3 scripts/recon.py ./challenge_file --mode file

# Manual
file challenge_file
strings challenge_file | grep -iE "ctf|flag|password|key"
xxd challenge_file | head -30
binwalk challenge_file
exiftool challenge_file
```

---

## Step 2 — By File Type

### 🖼️ Images (PNG / JPG / BMP)
```bash
# Metadata
exiftool image.jpg

# Steganography
steghide extract -sf image.jpg          # may need password
zsteg image.png                          # LSB steg (PNG/BMP)
stegsolve image.png                      # GUI — check all bit planes

# Binwalk extract
binwalk -e image.jpg
```

### 📦 ZIP / Archives
```bash
# Try to unzip
unzip archive.zip

# Crack password
fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt archive.zip
john --wordlist=/usr/share/wordlists/rockyou.txt zip.hash
```

### 🌐 PCAP Network Captures
```bash
# Open in Wireshark
wireshark capture.pcap

# CLI analysis
tcpdump -r capture.pcap
tshark -r capture.pcap -Y "http" -T fields -e http.request.uri

# Extract all HTTP objects: Wireshark → File → Export Objects → HTTP
# Follow TCP Stream: Right-click on packet → Follow → TCP Stream
```

### 💾 Disk Images
```bash
# List partitions
fdisk -l disk.img

# Mount
sudo mount -o loop,offset=$((512*2048)) disk.img /mnt/ctf

# Recover deleted files
foremost -i disk.img -o ./recovered
```

### 🧠 Memory Dumps
```bash
# Volatility 2
python2 vol.py -f mem.raw imageinfo
python2 vol.py -f mem.raw --profile=Win7SP1x64 pslist
python2 vol.py -f mem.raw --profile=Win7SP1x64 filescan | grep -i flag
python2 vol.py -f mem.raw --profile=Win7SP1x64 dumpfiles -Q 0xADDRESS -D ./

# Volatility 3
python3 vol.py -f mem.raw windows.pslist
python3 vol.py -f mem.raw windows.filescan | grep -i flag
```

### 🔍 OSINT
```
- Google: "site:target.com filetype:pdf"
- Wayback Machine: https://web.archive.org
- Shodan: https://shodan.io
- Reverse image search: images.google.com / TinEye
- Username lookup: https://namechk.com
- EXIF GPS: https://www.geoimgr.com
```

---

## Notes & Progress

```
[File type]  

[Found with] 

[Attempt 1]  
[Result]     

[Solution]   
```

---

## Flag
```
CTF{                                    }
```
