"""Extract text from research PDFs (WSL: python3 extract_pdfs.py <pdf> <name> ...) into research/<name>.txt,
collapsing the duplicated Thai combining marks that pdftotext produces for some fonts."""
import re
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
args = sys.argv[1:]
for pdf, name in zip(args[::2], args[1::2]):
    raw = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    s = re.sub(r"([ัิ-ฺ็-๎])\1+", r"\1", raw.replace("�", ""))
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    (OUT / f"{name}.txt").write_text(s, encoding="utf-8")
    print(name, len(s))
    print(s[:600].replace("\n", " | "))
