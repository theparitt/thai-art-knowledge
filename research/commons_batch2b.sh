#!/bin/bash
# Second pass: topics the first pass under-filled (WSL): bash commons_batch2.sh
cd "$(dirname "$0")" || exit 1
s() { python3 commons.py search "$1" "$2" "${3:-8}" > /dev/null 2>&1; echo "$1: $2"; }
c() { python3 commons.py cat "$1" "$2" "${3:-10}" > /dev/null 2>&1; echo "$1: $2"; }
c buddha "Category:Buddha images in Thailand" 12
s buddha "พระพุทธชินราช" 4
s buddha "Sukhothai walking Buddha bronze" 6
s buddha "Dvaravati Buddha statue" 6
s buddha "Ayutthaya period Buddha crowned" 6
s buddha "Lanna Buddha bronze Chiang Saen" 6
s himmapan "Garuda Wat Phra Kaew" 8
s himmapan "kinnari Wat Phra Kaew golden" 6
s himmapan "naga balustrade stairs temple Thailand" 8
s himmapan "yaksha Wat Phra Kaew" 6
s houses "Thai house" 10
s houses "Kalae" 6
s houses "Lanna house" 6
s temple "Ho Trai" 8
s temple "ใบเสมา" 6
s temple "Wat Phra That Lampang Luang" 6
s temple "Lanna wihan" 6
s crafts "Benjarong" 6
s crafts "เบญจรงค์" 6
s crafts "niello Thailand" 6
s crafts "mother-of-pearl door Thailand" 6
s crafts "Wat Arun porcelain decoration" 8
echo done2b
