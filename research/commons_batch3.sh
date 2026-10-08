#!/bin/bash
# Third pass: real ornament objects (museum pieces, stucco, lacquer), not logos (WSL): bash commons_batch3.sh
cd "$(dirname "$0")" || exit 1
s() { python3 commons.py search "$1" "$2" "${3:-8}" > /dev/null 2>&1; echo "$1: $2"; }
c() { python3 commons.py cat "$1" "$2" "${3:-10}" > /dev/null 2>&1; echo "$1: $2"; }
c ornament "Category:Lai Thai" 12
c ornament "Category:Kranok" 12
c ornament "Category:Thai ornaments" 12
c ornament "Category:Lai rot nam" 12
s ornament "Thai manuscript cabinet lacquer gold" 8
s ornament "Thai stucco decoration Ayutthaya" 8
s ornament "Thai gable stucco Wat Phutthaisawan" 6
s ornament "Thai lacquer box gold pattern museum" 6
s ornament "prachamyam motif" 4
s ornament "Thai pattern door Wat Pho stucco" 6
echo done3
