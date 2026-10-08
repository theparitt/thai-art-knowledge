#!/bin/bash
# Collect Commons candidates for every topic (WSL): bash commons_batch.sh
cd "$(dirname "$0")" || exit 1
s() { python3 commons.py search "$1" "$2" "${3:-8}" > /dev/null 2>&1; echo "$1: $2"; }
c() { python3 commons.py cat "$1" "$2" "${3:-10}" > /dev/null 2>&1; echo "$1: $2"; }
s roofs "Wat Pho gable roof tiers" 8
s roofs "Wat Phra Kaew ubosot roof" 8
s roofs "Wat Benchamabophit roof" 6
s roofs "Thai temple multi-tiered roof" 8
s prasat "Dusit Maha Prasat Throne Hall" 6
s prasat "Phra Mondop Wat Phra Kaew" 6
s prasat "Aphorn Phimok Prasat" 4
s prasat "busabok Thai" 6
s mondop "Wat Arun mondop" 10
s prang "Wat Arun prang" 8
s prang "Wat Arun Indra Erawan" 4
s prang "Wat Arun yaksha" 4
s prang "Wat Arun porcelain" 6
s chedi "Wat Chaiwatthanaram" 6
s chedi "Phra Si Rattana Chedi" 4
s chedi "Wat Phra Si Sanphet chedi" 4
s chedi "lotus bud chedi Sukhothai" 6
s chedi "redented chedi Thailand" 6
s bases "Wat Phra Kaew garuda base" 6
s bases "Thai temple base lotus moulding" 6
s gables "Thai temple pediment Narai Garuda" 6
s gables "Wat Phra Kaew pediment" 6
s gables "Wat Suthat pediment" 4
s laithai "lai rot nam" 8
s laithai "Thai lacquer gilded pattern" 8
s laithai "Thai ornament kranok" 8
s laithai "Wat Pho mother of pearl door" 6
s laithai "Thai stucco ornament temple" 8
s painting "Wat Suthat mural" 8
s painting "Wat Pho mural" 6
s painting "Ramakien mural Wat Phra Kaew" 6
s painting "Wat Suwannaram mural" 6
s painting "Wat Buddhaisawan mural" 6
s buddha "Phra Phuttha Chinnarat" 4
s buddha "walking Buddha Sukhothai" 6
s buddha "Dvaravati Buddha" 6
s buddha "Chiang Saen Buddha image" 6
s buddha "Ayutthaya crowned Buddha" 6
s buddha "U Thong Buddha" 4
s himmapan "garuda Wat Phra Kaew" 6
s himmapan "naga staircase Thai temple" 6
s himmapan "kinnari statue Wat Phra Kaew" 6
s himmapan "yaksha guardian Wat Phra Kaew" 6
s himmapan "Himmapan creatures" 6
s houses "Thai house Jim Thompson" 6
s houses "kalae house Chiang Mai" 6
s houses "traditional Thai house central" 6
s houses "Isan traditional house" 4
s houses "southern Thailand traditional house" 4
s temple "ho trai Wat Rakhang" 4
s temple "ho trai scripture library pond Thailand" 6
s temple "bai sema boundary stone" 6
s temple "Wat Phra That Lampang Luang viharn" 6
s temple "Lanna viharn interior" 6
s temple "sala Thai pavilion" 4
s crafts "Benjarong" 6
s crafts "Thai niello ware" 6
s crafts "mother of pearl inlay Thailand" 6
s crafts "Thai wood carving temple door" 6
s stairs "naga balustrade Thai temple stairs" 6
s stairs "kamphaeng kaeo Thai temple wall" 4
echo done
