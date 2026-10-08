#!/bin/bash
# Second pass: topics the first pass under-filled (WSL): bash commons_batch2.sh
cd "$(dirname "$0")" || exit 1
s() { python3 commons.py search "$1" "$2" "${3:-8}" > /dev/null 2>&1; echo "$1: $2"; }
c() { python3 commons.py cat "$1" "$2" "${3:-10}" > /dev/null 2>&1; echo "$1: $2"; }
s patterns "กระหนก" 8
s patterns "ลายกนก" 8
s patterns "ลายไทย" 10
s patterns "Thai pattern kanok" 8
s patterns "ประจำยาม" 6
s patterns "กระจัง" 6
s patterns "Thai ornament stucco pattern Wat" 8
s gables "หน้าบัน" 10
s gables "Thai temple gable tympanum" 8
s gables "pediment Wat Thailand Garuda Narai" 8
s gables "หน้าบัน วัด" 8
s bases "ฐานสิงห์" 6
s bases "Thai temple base Ayutthaya boat-shaped" 6
s bases "Wat Phra Kaew garuda naga base ubosot" 6
s redent "ย่อมุมไม้สิบสอง" 6
s redent "Wat Phu Khao Thong Ayutthaya chedi" 4
s redent "redented chedi Ayutthaya" 6
s windows "ซุ้มหน้าต่าง" 6
s windows "Thai temple window arch ornament" 8
s windows "Wat Ratchabophit door" 6
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
echo done
