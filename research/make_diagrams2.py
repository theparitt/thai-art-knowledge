"""More diagrams for the knowledge site (WSL: python3 make_diagrams2.py). Uses the helpers of make_diagrams.py."""
import math

import numpy as np
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle, FancyBboxPatch

from make_diagrams import fig, save, INK, RED, BLUE, GOLD


def four_families():
    f, ax = fig(13, 4.6, "การเขียนลายไทยแบ่ง 4 ตระกูล: กนก · นารี · กระบี่ · คชะ (เรียนกนกก่อน)")
    cols = [("กนก", "ลวดลาย เปลว ใบ ก้าน", RED), ("นารี", "มนุษย์ เทวดา", BLUE), ("กระบี่", "ยักษ์ ลิง อมนุษย์", GOLD),
            ("คชะ", "สัตว์ ช้าง ม้า หิมพานต์", "#2e7d32")]
    for i, (n, d, c) in enumerate(cols):
        x0 = i * 3.3
        ax.add_patch(FancyBboxPatch((x0, 0), 2.9, 3.0, boxstyle="round,pad=0.05", fc="#faf6ee", ec=c, lw=2))
        ax.text(x0 + 1.45, 2.55, n, ha="center", fontsize=18, color=c)
        ax.text(x0 + 1.45, 0.25, d, ha="center", fontsize=10.5)
        cx, cy = x0 + 1.45, 1.4
        if i == 0:
            ax.add_patch(MPoly([(cx - .6, cy - .7), (cx + .5, cy - .7), (cx - .6, cy + .9)], closed=True, fc="none", ec=c, lw=1.5))
            th = np.linspace(0, 2.2 * math.pi, 80)
            r = .1 + .05 * th
            ax.plot(cx - .1 + r * np.cos(th), cy - .4 + r * np.sin(th) * .8, color=c)
            ax.plot([cx - .45, cx - .3, cx - .5], [cy, cy + .5, cy + .85], color=c)
        elif i == 1:
            ax.add_patch(Circle((cx, cy + .45), .18, fc="none", ec=c, lw=1.5))
            ax.plot([cx - .08, cx, cx + .08], [cy + .6, cy + .9, cy + .6], color=c)
            ax.plot([cx, cx], [cy + .27, cy - .5], color=c, lw=1.5)
            ax.plot([cx - .35, cx, cx + .35], [cy - .75, cy - .5, cy - .75], color=c, lw=1.5)
            ax.plot([cx - .35, cx, cx + .35], [cy + .05, cy + .2, cy + .05], color=c, lw=1.5)
        elif i == 2:
            ax.add_patch(Circle((cx, cy + .35), .25, fc="none", ec=c, lw=1.5))
            ax.plot([cx - .1, cx - .08], [cy + .25, cy + .15], color=c)
            ax.plot([cx + .1, cx + .08], [cy + .25, cy + .15], color=c)
            ax.plot([cx - .5, cx - .25, cx], [cy + .8, cy + .1, cy - .7], color=c, lw=1.5)
            ax.plot([cx + .5, cx + .25, cx], [cy + .8, cy + .1, cy - .7], color=c, lw=1.5)
        else:
            ax.add_patch(MPoly([(cx - .7, cy - .1), (cx + .3, cy - .1), (cx + .4, cy + .4), (cx - .6, cy + .45)], closed=True,
                               fc="none", ec=c, lw=1.5))
            ax.plot([cx + .4, cx + .65, cx + .6, cx + .7], [cy + .3, cy + .1, cy - .4, cy - .6], color=c, lw=1.5)
            for lx in (cx - .6, cx - .3, cx, cx + .25):
                ax.plot([lx, lx], [cy - .1, cy - .7], color=c, lw=1.5)
    ax.text(6.4, -0.6, "ที่มา: วิกิพีเดีย ศิลปะไทย; thaiarchiculture (แผนภาพสัญลักษณ์ ไม่ใช่ลายจริง)", ha="center", fontsize=9.5)
    ax.set_xlim(-0.3, 13.2)
    ax.set_ylim(-0.9, 3.2)
    save(f, "13_four_families.png")


def row_patterns():
    f, ax = fig(13, 6.2, "การเรียงลายตามตำแหน่ง (แผนภาพโครงสร้าง)")
    y = 4.6
    ax.add_patch(Rectangle((0, y), 12, 0.9, fc="#f3e6cf", ec=INK))
    for x in np.arange(0.6, 11, 1.6):
        cx = x + .2
        ax.add_patch(MPoly([(cx, y + .1), (cx + .35, y + .45), (cx, y + .8), (cx - .35, y + .45)], closed=True, fc="#e7c98f", ec=RED))
        ax.plot([cx + .4, cx + 1.2], [y + .45, y + .45], color=GOLD, lw=1.2)
    ax.text(12.2, y + .45, "ลายหน้ากระดาน: แถบนอน ประจำยามคั่นจังหวะ", va="center", fontsize=10.5)
    y = 3.1
    ax.add_patch(Rectangle((0, y), 12, .25, fc="#f3e6cf", ec=INK))
    for x in np.arange(0, 12, .6):
        ax.add_patch(MPoly([(x, y + .25), (x + .6, y + .25), (x + .45, y + .6), (x + .3, y + 1.0), (x + .15, y + .6)],
                           closed=True, fc="#e7c98f", ec=INK, lw=.8))
    ax.text(12.2, y + .5, "กระจังเรียง: ขอบบนของบัวหงาย", va="center", fontsize=10.5)
    for x0 in (0.5, 3.0):
        ax.add_patch(Rectangle((x0, 0), 1.2, 2.6, fc="#f3e6cf", ec=INK))
        ax.add_patch(MPoly([(x0 + .1, 2.5), (x0 + 1.1, 2.5), (x0 + .6, 1.6)], closed=True, fc="#e7c98f", ec=RED))
        ax.add_patch(MPoly([(x0 + .1, .1), (x0 + 1.1, .1), (x0 + .6, 1.0)], closed=True, fc="#e7c98f", ec=RED))
    ax.text(0.2, -0.4, "ลายกรวยเชิง: สามเหลี่ยมยาวที่หัวเสาและโคนเสา (กลางเสาใช้รักร้อย)", fontsize=10.5)
    th = np.linspace(0, 4 * math.pi, 400)
    ax.plot(6.2 + th / (4 * math.pi) * 5.4, 1.3 + .7 * np.sin(th), color=RED, lw=1.8)
    for k in range(1, 8):
        t = k * math.pi / 2
        x = 6.2 + t / (4 * math.pi) * 5.4
        yy = 1.3 + .7 * math.sin(t)
        s = 1 if k % 2 else -1
        th2 = np.linspace(0, 1.6 * math.pi, 60)
        r = .05 + .06 * th2
        ax.plot(x + r * np.cos(th2) * s, yy + .25 * s + r * np.sin(th2), color=GOLD, lw=1.2)
    ax.text(6.2, -1.0, "ลายก้านขด: ก้านขดเป็นวงต่อเนื่อง กระหนกแตกออกจากก้าน", fontsize=10.5)
    ax.set_xlim(-0.3, 17.5)
    ax.set_ylim(-1.4, 5.8)
    save(f, "14_row_patterns.png")


def mural_layout():
    f, ax = fig(13, 6.5, "แบบแผนจิตรกรรมฝาผนังอุโบสถ (อยุธยาตอนปลาย–รัตนโกสินทร์ตอนต้น)")

    def wall(x0, w, title):
        ax.add_patch(Rectangle((x0, 0), w, 5, fc="#fbf8f2", ec=INK))
        ax.text(x0 + w / 2, 5.25, title, ha="center", fontsize=11)
    wall(0, 3.2, "ผนังสกัดหลัง (หลังพระประธาน)")
    ax.add_patch(Rectangle((0.1, 0.1), 3.0, 4.8, fc="#e3ecf8", ec="none"))
    ax.text(1.6, 2.6, "ไตรภูมิ\nโลกสัณฐาน\n(หรือเสด็จลงจาก\nดาวดึงส์)", ha="center", va="center", fontsize=11)
    wall(3.6, 6.0, "ผนังด้านยาว (ผนังแป)")
    ax.add_patch(Rectangle((3.7, 3.4), 5.8, 1.5, fc="#f8eccd", ec="none"))
    ax.text(6.6, 4.15, "เทพชุมนุม (แถวเทวดาหันไปทางพระประธาน)", ha="center", va="center", fontsize=10.5)
    for i in range(3):
        x = 4.0 + i * 1.9
        ax.add_patch(Rectangle((x, 1.0), 0.6, 2.0, fc="#cfd8dc", ec=INK))
        if i < 2:
            ax.add_patch(Rectangle((x + .7, .2), 1.1, 3.0, fc="#f1e0e0", ec="none"))
            ax.text(x + 1.25, 1.7, "พุทธ\nประวัติ /\nทศชาติ", ha="center", va="center", fontsize=9.5)
    ax.text(4.05, .6, "หน้าต่าง", fontsize=8.5, color="#555")
    wall(10.0, 3.2, "ผนังสกัดหน้า (ด้านประตู)")
    ax.add_patch(Rectangle((10.1, 1.6), 3.0, 3.3, fc="#f6dede", ec="none"))
    ax.text(11.6, 3.3, "มารผจญ", ha="center", va="center", fontsize=12)
    ax.add_patch(Rectangle((11.1, 0), 1.0, 1.5, fc="#cfd8dc", ec=INK))
    ax.text(11.6, .7, "ประตู", ha="center", fontsize=9)
    ax.text(6.6, -0.6, "พระประธานปางมารวิชัยหันหน้าไปผนังสกัดหน้า ภาพมารผจญจึงอยู่ตรงหน้าพระ · ที่มา: S22 (อ้าง สันติ เล็กสุขุม 2014)",
            ha="center", fontsize=10)
    ax.set_xlim(-0.3, 13.5)
    ax.set_ylim(-1.0, 5.7)
    save(f, "15_mural_wall_layout.png")


def regional_roofs():
    f, ax = fig(13, 4.6, "หลังคาเรือนไทย 4 ภาค (แผนภาพด้านหน้า)")

    def base(x0):
        ax.add_patch(Rectangle((x0 - 1.1, 0.9), 2.2, 1.0, fc="#efe1c6", ec=INK))
        for px in (x0 - 1.0, x0 + 1.0):
            ax.plot([px, px], [0, .9], color=INK, lw=2)
    t = np.linspace(0, 1, 30)
    x = 0
    base(x)
    ax.plot(x - 1.5 + 1.5 * t, 1.9 + 2.2 * t - .25 * np.sin(math.pi * t), color="#7a5a2a", lw=3)
    ax.plot(x + 1.5 - 1.5 * t, 1.9 + 2.2 * t - .25 * np.sin(math.pi * t), color="#7a5a2a", lw=3)
    for sx in (-1, 1):
        ax.plot([x + sx * 1.5, x + sx * 1.75, x + sx * 1.65], [1.9, 2.05, 2.3], color="#7a5a2a", lw=3)
    ax.text(x, -0.75, "ภาคกลาง: จั่วสูงชัน ปั้นลมจอมแห\nตัวเหงา ใต้ถุนสูง", ha="center", fontsize=10)
    x = 3.6
    base(x)
    ax.plot([x - 1.6, x, x + 1.6], [1.9, 3.4, 1.9], color="#7a5a2a", lw=3)
    ax.plot([x - .5, x + .45], [4.2, 3.0], color="#7a5a2a", lw=3)
    ax.plot([x + .5, x - .45], [4.2, 3.0], color="#7a5a2a", lw=3)
    ax.text(x, -0.75, "ภาคเหนือ: เรือนกาแล\nไม้ไขว้ยอดจั่ว ชายคาต่ำ", ha="center", fontsize=10)
    x = 7.2
    base(x)
    ax.plot([x - 1.45, x, x + 1.45], [1.9, 3.3, 1.9], color="#7a5a2a", lw=3)
    ax.text(x, -0.75, "ภาคอีสาน: จั่วเรียบ เรือนทึบ\nมีเกย (ระเบียงเปิด)", ha="center", fontsize=10)
    x = 10.8
    base(x)
    ax.add_patch(MPoly([(x - 1.6, 1.9), (x + 1.6, 1.9), (x + .6, 3.0), (x - .6, 3.0)], closed=True, fc="none", ec="#7a5a2a", lw=3))
    ax.text(x, -0.75, "ภาคใต้: ปั้นหยา / มนิลา\nต้านลม เสาตั้งบนตีนเสา", ha="center", fontsize=10)
    ax.text(5.4, -1.75, "ที่มา: วิกิพีเดีย เรือนไทย 4 ภาค (แผนภาพแนวคิด)", ha="center", fontsize=9.5)
    ax.set_xlim(-2, 12.8)
    ax.set_ylim(-2.1, 4.6)
    save(f, "16_regional_house_roofs.png")


if __name__ == "__main__":
    for fn in (four_families, row_patterns, mural_layout, regional_roofs):
        fn()
