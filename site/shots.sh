#!/bin/bash
# Screenshot built pages with headless Chrome for a visual check (WSL): bash site/shots.sh
cd "$(dirname "$0")/.." || exit 1
python3 -m http.server 8765 -d dist >/dev/null 2>&1 &
SRV=$!
sleep 1
for p in index lai-thai-catalogue roofs spires; do
  timeout 40 google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=1280,1800 \
    --screenshot="research/_shot_$p.png" "http://localhost:8765/$p.html" >/dev/null 2>&1
done
timeout 40 google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=390,1500 \
  --screenshot="research/_shot_mobile.png" "http://localhost:8765/index.html" >/dev/null 2>&1
kill $SRV
ls -la research/_shot_*
