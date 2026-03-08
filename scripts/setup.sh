#!/bin/bash
# ============================================================
# CTF Zero to Hero — Environment Setup Script
# Run: bash scripts/setup.sh
# ============================================================

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ██████╗████████╗███████╗"
echo "  ██╔════╝╚══██╔══╝██╔════╝"
echo "  ██║        ██║   █████╗  "
echo "  ██║        ██║   ██╔══╝  "
echo "  ╚██████╗   ██║   ██║     "
echo "   ╚═════╝   ╚═╝   ╚═╝     "
echo -e "  Zero to Hero Setup${NC}"
echo ""

echo -e "${YELLOW}[*] Updating package lists...${NC}"
sudo apt-get update -qq

echo -e "${YELLOW}[*] Installing system tools...${NC}"
sudo apt-get install -y -qq \
  binwalk \
  exiftool \
  wireshark \
  foremost \
  steghide \
  hashcat \
  john \
  nmap \
  netcat-openbsd \
  curl \
  wget \
  python3 \
  python3-pip \
  ltrace \
  strace \
  gdb \
  file \
  strings

echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip3 install -q \
  pwntools \
  requests \
  beautifulsoup4 \
  pycryptodome \
  sympy \
  xortool \
  flask

echo -e "${YELLOW}[*] Installing GDB plugins (pwndbg)...${NC}"
if [ ! -d "$HOME/pwndbg" ]; then
  git clone https://github.com/pwndbg/pwndbg "$HOME/pwndbg" -q
  cd "$HOME/pwndbg" && ./setup.sh -q
  cd -
fi

echo -e "${GREEN}[✓] All tools installed successfully!${NC}"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "  1. Install Burp Suite:  https://portswigger.net/burp/communitydownload"
echo "  2. Install Ghidra:      https://ghidra-sre.org"
echo "  3. Open CyberChef:      https://gchq.github.io/CyberChef"
echo ""
echo -e "${GREEN}Happy hacking! 🏴${NC}"
