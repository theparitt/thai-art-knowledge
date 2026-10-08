"""Annotated copies of key reference photos: numbered markers + a legend naming each part.
WSL: python3 annotate_refs.py   -> images/annotated/*.png   (internal reference only)"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "images" / "reference"
OUT = ROOT / "images" / "annotated"
OUT.mkdir(parents=True, exist_ok=True)
for f in font_manager.findSystemFonts():
    if f.replace(" ", "").endswith("THSarabunNew.ttf"):
        font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["TH Sarabun New"]

# (file, title, [(x, y, label), ...]) — x, y in pixels of the reference JPEG
JOBS = [
    ("43_son_lot_gables_and_naga_heads.jpg", "จั่วที่ลดลงมาด้านหน้า 3 ชั้น และชายคาที่ลดเป็นขั้น",
     [(235, 255, "ช่อฟ้า ของจั่วหน้า (ต่ำสุด)"), (570, 210, "ช่อฟ้า ของจั่วกลาง (สูงกว่า)"),
      (845, 130, "ช่อฟ้า ของจั่วหลัง (สูงสุด ใหญ่สุด)"), (330, 560, "ป้านลม 3 เส้นขนานกัน ความชันเท่ากัน"),
      (560, 730, "ผืนหลังคา (ตับ) แต่ละผืนมีกรอบสีของตัวเอง"), (410, 800, "หางหงส์ ที่ปลายป้านลมของชั้นบน"),
      (480, 1040, "หางหงส์ ที่ขั้นชายคาลดลงมา"), (205, 1270, "หางหงส์ ทุกขั้นที่ลดมีหัวนาคของตัวเอง"),
      (300, 1060, "หน้าบัน (เว้าลึกเข้าไปจากป้านลม)")]),
    ("42_lamyong_detail_bai_raka_ngouang_aiyara.jpg", "เครื่องลำยอง: ตัวรวยแบบนาคสะดุ้ง",
     [(330, 140, "ใบระกา: ครีบเรียงบนสันตัวรวย"), (300, 330, "งวงไอยรา: เกี่ยวกระหวัดลงใต้แป"),
      (560, 205, "หางหงส์: เศียรนาคเชิดขึ้น (ตับบน)"), (728, 360, "หางหงส์ (ตับที่ 2)"), (872, 520, "หางหงส์ (ตับที่ 3)"),
      (120, 400, "หน้าบัน: ลายพรรณพฤกษาปิดทอง"), (560, 470, "ตัวรวยพักบนแป เป็นจังหวะ (นาคสะดุ้ง)")]),
    ("41_wat_pho_roof_lot_and_son_side.jpg", "วัดโพธิ์ มองด้านข้าง: จั่วลดที่ปลายอาคาร และหลังคาตับล่าง",
     [(150, 330, "หลังคาช่วงประธาน (สูงสุด)"), (912, 190, "ช่อฟ้า จั่วลดชั้นที่ 1"), (985, 195, "ช่อฟ้า จั่วลดชั้นที่ 2"),
      (1072, 195, "ช่อฟ้า จั่วลดชั้นที่ 3 (ปลายสุด ต่ำสุด)"), (700, 330, "ผืนหลังคาจั่วด้านปลาย"),
      (600, 545, "หลังคาตับล่าง (ปีกนก/ซ้อนล่าง) ลาดต่ำรอบอาคาร"), (600, 670, "ตับล่างสุด ลดลงอีกขั้น")]),
    ("31_phra_mondop_wat_phra_kaew_prasat_roof.jpg", "พระมณฑปวัดพระแก้ว: หลังคาซ้อน 4 ทิศ + ยอดงอกจากกลาง",
     [(196, 106, "ยอดทรงมณฑป: ชั้นเชิงกลอนซ้อน 7 ชั้น"), (196, 150, "เรือนยอด เริ่มจากกลางหลังคา"),
      (217, 171, "จั่วด้านหน้า ซ้อนชั้น"), (102, 195, "จั่วด้านข้าง (ต่ำกว่า)"), (135, 210, "หลังคาตับล่าง"),
      (205, 265, "ผนังมีซุ้มทุกช่อง"), (164, 176, "ช่อฟ้า")]),
    ("40_dusit_maha_prasat_front_son_gables.jpg", "พระที่นั่งดุสิตมหาปราสาท: จั่วซ้อนด้านหน้า + ยอดปราสาท",
     [(195, 235, "ยอดปราสาท: ชั้นซ้อนมีซุ้มบรรพแถลงทุกชั้น"), (229, 372, "ครุฑที่หน้าเรือนยอด ตรงจุดที่หลังคามาบรรจบ"),
      (132, 400, "หน้าบันจั่วหน้า (ผืนหน้าต่ำสุด)"), (151, 316, "ป้านลมของจั่วซ้อนชั้นหลัง ขนานกัน"),
      (319, 291, "ช่อฟ้า ของหลังคาแขนข้าง")]),
    ("14_wat_arun_mondop_long_face_porch_and_wings.jpg", "มณฑปทิศวัดอรุณ ด้านยาว: มุขกลาง + ปีกซ้ายขวา",
     [(295, 250, "หน้าต่างลายเขียว บนมุขกลาง (ยื่นออกมา)"), (105, 330, "หน้าต่างปีก"), (480, 330, "หน้าต่างปีก"),
      (290, 100, "จั่วมุขกลาง + ยอด"), (80, 230, "หลังคาปีก (ต่ำกว่า)"), (183, 519, "แถบเทวดาแบก ยื่นตามมุข"),
      (477, 726, "ฐานซุ้มโค้ง"), (477, 829, "ฐานลายกระเบื้องฉลุ")]),
]

for name, title, marks in JOBS:
    im = Image.open(REF / name)
    w, h = im.size
    figw = 13
    fig = plt.figure(figsize=(figw, figw * 0.62), dpi=110)
    ax_img = fig.add_axes([0.0, 0.0, 0.58, 0.93])
    ax_img.imshow(im)
    ax_img.axis("off")
    ax_leg = fig.add_axes([0.6, 0.0, 0.4, 0.93])
    ax_leg.axis("off")
    for i, (x, y, lab) in enumerate(marks, 1):
        ax_img.plot(x, y, "o", ms=17, mfc="#ffd400", mec="#b8322a", mew=2.2)
        ax_img.text(x, y, str(i), ha="center", va="center", fontsize=13, color="#b8322a", fontweight="bold")
        ax_leg.text(0.0, 1 - i * 0.085, f"{i}. {lab}", fontsize=18, va="top", transform=ax_leg.transAxes)
    fig.suptitle(title, fontsize=22, x=0.02, ha="left")
    fig.savefig(OUT / name.replace(".jpg", "_annotated.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)
