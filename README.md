# 🏴 CTF Zero to Hero

> **A complete beginner's resource kit for Capture The Flag competitions.**  
> Scripts, checklists, payload lists, challenge templates, and the full session presentation — everything you need to go from zero to your first flag.

![CTF](https://img.shields.io/badge/CTF-Beginner%20Friendly-00D4AA?style=for-the-badge)
![Categories](https://img.shields.io/badge/Categories-Web%20%7C%20Crypto%20%7C%20Pwn%20%7C%20RE%20%7C%20Forensics%20%7C%20Misc-4CC9F0?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-FFD166?style=for-the-badge)

---

## 📁 Repository Structure

```
ctf-zero-to-hero/
├── 📊 presentation/          # Full beginner CTF slide deck (.pptx)
├── 🌐 challenges/
│   ├── web/                  # Web exploitation challenge notes & templates
│   ├── crypto/               # Cryptography solving templates
│   ├── pwn/                  # Binary exploitation templates
│   ├── re/                   # Reverse engineering notes
│   ├── forensics/            # Forensics investigation templates
│   └── misc/                 # Miscellaneous challenge notes
├── 🛠️ scripts/               # Automation & helper scripts
├── 🔧 tools/                 # Tool setup guides
└── 📦 resources/
    ├── wordlists/            # Common wordlists & references
    └── payloads/             # Payload collections per category
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ctf-zero-to-hero.git
cd ctf-zero-to-hero
```

### 2. Install core tools
```bash
# Python tools
pip3 install pwntools requests

# Kali Linux (recommended VM)
# https://www.kali.org/get-kali/

# Or use the setup script
bash scripts/setup.sh
```

### 3. Open the presentation
Find `presentation/CTF_Beginners.pptx` — this is your complete beginner guide.

---

## 🗺️ Beginner Attack Order

| Priority | Category | Difficulty | Why Start Here? |
|----------|----------|------------|-----------------|
| 1st | ⚙️ Misc | ⭐ | Quick wins, creative thinking |
| 2nd | 🌐 Web | ⭐⭐ | Intuitive — you know websites |
| 3rd | 🕵️ Forensics | ⭐⭐ | Tools do the heavy lifting |
| 4th | 🔐 Crypto | ⭐⭐⭐ | Pattern recognition + CyberChef |
| 5th | 🔍 RE | ⭐⭐⭐ | Needs practice, invest time |
| 6th | 💥 Pwn | ⭐⭐⭐⭐ | Hardest — tackle last |

---

## 🧰 Essential Tools

| Tool | Category | Install |
|------|----------|---------|
| [CyberChef](https://gchq.github.io/CyberChef) | Crypto / Encoding | Browser — no install |
| [Burp Suite](https://portswigger.net/burp) | Web | Download + configure proxy |
| [Ghidra](https://ghidra-sre.org) | Reverse Engineering | Download + Java required |
| [Wireshark](https://wireshark.org) | Forensics | `apt install wireshark` |
| pwntools | Pwn | `pip3 install pwntools` |
| binwalk | Forensics | `apt install binwalk` |
| hashcat | Crypto | `apt install hashcat` |

---

## 🏋️ Practice Platforms

- 🟢 **[PicoCTF](https://picoctf.org)** — Best for absolute beginners
- 🔵 **[HackTheBox](https://hackthebox.com)** — Machines + CTF-style challenges
- 🟡 **[TryHackMe](https://tryhackme.com)** — Guided learning paths
- 🔴 **[OverTheWire](https://overthewire.org)** — Linux & wargame fundamentals
- 📅 **[CTFtime.org](https://ctftime.org)** — Upcoming real CTF events calendar

---

## 📖 How to Use This Repo

1. **Before a CTF** — read through the relevant `challenges/` folder for your target categories
2. **During a CTF** — use scripts in `scripts/` to speed up recon and enumeration
3. **After a CTF** — write up your solutions and add them to the relevant category folder

---

## 🤝 Contributing

Found a useful script, payload, or tip? PRs welcome!

1. Fork the repo
2. Create a branch: `git checkout -b feat/my-tip`
3. Commit your changes
4. Open a Pull Request

---

## ⚠️ Disclaimer

This repository is for **educational purposes only**. Only use these techniques on systems you own or have explicit permission to test. Unauthorized hacking is illegal.

---

## 📄 License

MIT — see [LICENSE](LICENSE)
