"""Explanatory diagrams for the Thai architecture docs (WSL: python3 make_diagrams.py).
Schematic, drawn from the sources cited in each doc file; not measured drawings. Output: images/diagrams/*.png"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "derived_diagrams"
OUT.mkdir(parents=True, exist_ok=True)
for f in font_manager.findSystemFonts():
    if f.replace(" ", "").endswith("THSarabunNew.ttf"):
        font_manager.fontManager.addfont(f)
plt.rcParams["font.family"] = ["TH Sarabun New"]      # Thai + Latin digits in one font
TEXT_SCALE = 1.45                                      # Sarabun has a small x-height
INK, RED, BLUE, GOLD, GREY = "#222222", "#b8322a", "#2a5bb8", "#b8860b", "#9a9a9a"


def fig(w=10, h=7, title=""):
    f, ax = plt.subplots(figsize=(w, h), dpi=130)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=15, pad=12)
    return f, ax


def save(f, name):
    import matplotlib.text as mtext
    for t in f.findobj(mtext.Text):
        t.set_fontsize(t.get_fontsize() * TEXT_SCALE)
    f.savefig(OUT / name, bbox_inches="tight", facecolor="white")
    plt.close(f)
    print("wrote", name)


def label(ax, x, y, text, tx, ty, color=INK, size=10.5, ha="left"):
    ax.annotate(text, (x, y), (tx, ty), fontsize=size, color=color, ha=ha, va="center",
                arrowprops=dict(arrowstyle="-", color=color, lw=0.8))


# ---------------------------------------------------------------- 1. ซ้อน: rear gable wider and higher, parallel
def son():
    f, ax = fig(12, 7.5, "จั่วซ้อนกันในแนวลึก (กฎที่ผู้ดูแลยืนยัน): ผืนหลังกว้างกว่า สูงกว่า ความชันเท่ากัน ป้านลมขนานกัน")
    pitch = 1.25
    layers = [(0.0, 0.0, "จั่วผืนหน้า (ซ้อนที่ 1) ต่ำสุด"), (1.6, 1.0, "ซ้อนที่ 2"), (3.2, 2.0, "ซ้อนที่ 3 (หลังคาประธาน)")]
    for i, (off, lift, name) in list(enumerate(layers))[::-1]:
        b = 4.0 + off                       # half width at its own eave
        z0 = lift * 0.9                     # its eave is a little higher (ลด) but the lines stay parallel
        h = b * pitch
        tri = [(-b, z0), (b, z0), (0, z0 + h)]
        ax.add_patch(MPoly(tri, closed=True, fc=["#f4e3c8", "#ecd2a8", "#e3c08c"][i], ec=INK, lw=1.4, zorder=3 - i))
        # bargeboard (ป้านลม) band
        for s in (-1, 1):
            ax.plot([s * b, 0], [z0, z0 + h], color=RED, lw=3.2, zorder=3 - i + 0.1)
            # หางหงส์ at the foot, pointing up
            ax.plot([s * b, s * (b + 0.15), s * (b + 0.05)], [z0, z0 + 0.45, z0 + 0.8], color=GOLD, lw=3, zorder=5)
        # ช่อฟ้า at the apex
        ax.plot([0, 0.1, 0.35, 0.25], [z0 + h, z0 + h + 0.55, z0 + h + 1.0, z0 + h + 1.25], color=GOLD, lw=3, zorder=6)
        ax.text(b + 0.4, z0 + 0.2 + 0.1 * i, name, fontsize=10.5, va="bottom")
    ax.text(0, -1.1, "มองตรงที่ด้านจั่ว: กรอบสามเหลี่ยมของผืนหลังอยู่นอกผืนหน้าทั้งสองข้างและสูงกว่า\n"
                     "แต่ละผืนมีช่อฟ้าและหางหงส์ของตัวเอง  ผิด: ห้ามทำผืนหลังเล็กหรือแคบกว่าผืนหน้า",
            ha="center", fontsize=11)
    ax.set_xlim(-9, 13)
    ax.set_ylim(-2, 12)
    save(f, "01_son_gable_layers.png")


# ---------------------------------------------------------------- 2. ซ้อน = nested gable houses (ราชบัณฑิตยสภา)
def son_section():
    f, ax = fig(12, 6.5, "ซ้อน ตามคำอธิบายราชบัณฑิตยสภา: เรือนจั่วหลายหลังลดหลั่นซ้อนกัน ตัดฝาออกเหลือหลังคาที่ร่นลงมาซ้อนกัน")
    k = 1.1                                              # one pitch for all: the bargeboards run parallel
    houses = [(7.2, 0.6, "เรือนนอก (ซ้อนล่าง)"), (5.4, 3.6, "เรือนกลาง"), (3.6, 6.6, "เรือนใน = หลังคาประธาน (สูงสุด)")]
    for i, (b, e, name) in enumerate(houses):           # outer first, inner on top
        h = b * k
        ax.add_patch(MPoly([(-b, e), (b, e), (0, e + h)], closed=True, fc=["#f4e3c8", "#ecd2a8", "#e3c08c"][i],
                           ec=INK, lw=1.2, zorder=i))
        for sx in (-1, 1):
            ax.plot([sx * b, 0], [e, e + h], color=RED, lw=2.6, zorder=i + 0.5)
            ax.plot([sx * b, sx * (b + 0.12), sx * (b + 0.02)], [e, e + 0.45, e + 0.8], color=GOLD, lw=3, zorder=5)
            ax.plot([sx * (b - 0.5), sx * (b - 0.5)], [0, e], color=GREY, ls="--", lw=1)
        ax.text(b + 0.35, e, name, fontsize=10, va="center")
    ax.plot([-9, 9], [0, 0], color=INK, lw=1)
    ax.text(0, -1.9, "ความชันเท่ากันทุกผืน: เรือนในผนังสูงสุด ยอดจั่วสูงสุด เรือนนอกกว้างกว่าแต่ต่ำกว่า มองที่ด้านจั่วจึงเห็นป้านลมเป็นขั้นขนานกัน\n"
                     "ไล่ลงมาด้านนอก แต่ละขั้นมีหางหงส์ของตัวเอง (เทียบรูปอ้างอิง 42, 43)  เส้นประ = ฝาเรือนที่ตัดออก\n"
                     "ที่มา: วารสารราชบัณฑิตยสภา ปีที่ 40 ฉบับที่ 2 (2558) หน้า 213", ha="center", fontsize=10)
    ax.set_xlim(-10, 14)
    ax.set_ylim(-2.6, 11)
    save(f, "02_son_nested_houses.png")


# ---------------------------------------------------------------- 3. ลด along the length + ตับ steps on the slope
def lot():
    f, ax = fig(13, 5.5, "ลด: หลังคาช่วงกลางสูงสุด ช่วงปลายลดต่ำลงทีละชั้น (มองด้านข้างอาคาร)")
    segs = [(-9, -6, 3.0), (-6, -3.5, 4.0), (-3.5, 3.5, 5.0), (3.5, 6, 4.0), (6, 9, 3.0)]
    for x0, x1, top in segs:
        ax.add_patch(MPoly([(x0, 1.0), (x1, 1.0), (x1, top), (x0, top)], closed=True, fc="#e9cfa3", ec=INK, lw=1.3))
        ax.plot([x0, x1], [top, top], color=RED, lw=2.5)
    for x, top in [(-9, 3.0), (-6, 4.0), (-3.5, 5.0), (3.5, 5.0), (6, 4.0), (9, 3.0)]:
        ax.plot([x, x + (0.25 if x > 0 else -0.25)], [top, top + 0.8], color=GOLD, lw=3)
    ax.add_patch(Rectangle((-9.5, 0), 19, 1.0, fc="#ddd", ec=INK))
    ax.text(0, 5.4, "ช่วงประธาน", ha="center", fontsize=11)
    ax.text(-7.5, 3.4, "ลด 2", ha="center", fontsize=10)
    ax.text(-4.75, 4.4, "ลด 1", ha="center", fontsize=10)
    ax.text(0, -0.8, "สันของช่วงที่ลด ต่ำกว่าหรือสั้นกว่าช่วงถัดเข้าไป = \"หลังคาลด\" แต่ละช่วงที่ปลายมีจั่วและช่อฟ้าของตัวเอง",
            ha="center", fontsize=10.5)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1.5, 6.5)
    save(f, "03_lot_roof_steps.png")


# ---------------------------------------------------------------- 4. เครื่องลำยอง on the purlins (สมใจ นิ่มเล็ก)
def lamyong():
    f, ax = fig(11, 8.5, "เครื่องลำยอง (ครึ่งหน้าจั่ว): ตัวรวยพาดบนแปลาน")
    b, h = 8.0, 8.0
    ax.add_patch(MPoly([(0, 0), (b, 0), (0, h)], closed=True, fc="#f3e6cf", ec=GREY, lw=1))
    # purlins (แปลาน) seen end-on
    for t, name in [(0.08, "แปหัวเสา"), (0.32, "แปลานตัวที่ 1"), (0.58, "แปลานตัวที่ 2 = แปงวง"), (1.0, "อกไก่")]:
        x, y = b * (1 - t), h * t
        ax.add_patch(Rectangle((x - 0.18, y - 0.45), 0.36, 0.36, fc="#8b5a2b", ec=INK, zorder=4))
        ax.text(x + 0.45, y - 0.6, name, fontsize=9.5, color="#5a3a1a")
    # the naga body (ตัวรวย) with a dip (สะดุ้ง) at purlin 1 and a hook (งวง) at purlin 2
    pts = [(b + 0.6, 0.3), (b * 0.86, h * 0.14), (b * 0.70, h * 0.27), (b * 0.66, h * 0.34), (b * 0.6, h * 0.36),
           (b * 0.47, h * 0.5), (b * 0.40, h * 0.62), (b * 0.36, h * 0.6), (b * 0.30, h * 0.70), (0.0, h)]
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=RED, lw=5, zorder=5, solid_capstyle="round")
    # ใบระกา fins along the top
    for t in [0.12 + 0.07 * k for k in range(12)]:
        x, y = b * (1 - t), h * t
        ax.plot([x, x - 0.15], [y + 0.25, y + 0.85], color=GOLD, lw=2.2, zorder=6)
    # ช่อฟ้า and หางหงส์
    ax.plot([0, 0.15, 0.55, 0.4], [h, h + 1.0, h + 1.8, h + 2.2], color=GOLD, lw=4, zorder=6)
    ax.plot([b + 0.6, b + 0.95, b + 1.1, b + 0.85], [0.3, 0.9, 1.6, 2.0], color=GOLD, lw=4, zorder=6)
    label(ax, 0.4, h + 1.9, "ช่อฟ้า: เหนืออกไก่ มีอก ปาก หงอน", -5.5, h + 2.3)
    label(ax, b * 0.2, h * 0.82, "ใบระกา: ครีบบนสันตัวรวย", -5.5, h * 0.82)
    label(ax, b * 0.40, h * 0.62, "งวง / งวงไอยรา: เกี่ยวกระหวัดแปตัวที่ 2 (แปงวง)", -5.5, h * 0.55)
    label(ax, b * 0.66, h * 0.33, "นาคสะดุ้ง: ช่วงที่พักบนแปลานตัวที่ 1", -5.5, h * 0.28)
    label(ax, b + 1.0, 1.6, "หางหงส์: เศียรนาค หันไปด้านข้างจั่ว\n(ถ้าเอี้ยวหันมาด้านหน้าจั่ว = นาคเบือน)", -5.5, 1.0)
    ax.text(4.0, -1.4, "ตัวรวยทั้งเส้น = ลำยอง / ตัวลำยอง  ·  รวมช่อฟ้า ใบระกา หางหงส์ (และตับที่ 2, 3, 4) = เครื่องลำยอง\n"
                       "ที่มา: สมใจ นิ่มเล็ก (2539) เครื่องบนและงานประดับของสถาปัตยกรรมไทย อ้างใน ภาสกร แสงสว่าง (2560)",
            ha="center", fontsize=10)
    ax.set_xlim(-6, 11)
    ax.set_ylim(-2.2, 11)
    save(f, "04_lamyong_on_purlins.png")


# ---------------------------------------------------------------- 5. ช่อฟ้า types
def chofa_types():
    f, ax = fig(12, 4.8, "แบบของช่อฟ้า (ตามรูปปากและคอ)")
    def neck(x0, pts, name, note):
        xs = [x0 + p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, color=GOLD, lw=6, solid_capstyle="round")
        ax.add_patch(Rectangle((x0 - 1.4, -0.5), 2.0, 0.5, fc="#c97", ec=INK))
        ax.text(x0, -1.2, name, ha="center", fontsize=11.5)
        ax.text(x0, -1.9, note, ha="center", fontsize=9.5, color="#555")
    neck(0, [(0, 0), (0.2, 1.4), (0.5, 2.8), (0.45, 3.8), (0.15, 4.2), (-0.05, 3.9)], "ปากนก / ปากครุฑ", "ชะลูดสูง หงอนเพรียว ปากงุ้มเข้า")
    neck(5, [(0, 0), (0.2, 1.4), (0.5, 2.8), (0.45, 3.8), (0.75, 4.25), (1.15, 4.3)], "ปากปลา / ปากหงส์", "ปากงอนออก")
    neck(10, [(0, 0), (0.2, 0.9), (0.45, 1.6), (0.75, 1.95), (1.05, 1.9)], "หัวนกเจ่า", "ไม่สูง คอสั้น หงอนเตี้ย")
    ax.text(5, 5.2, "ช่อฟ้าอยู่ในระนาบตั้งของสันหลังคา (ตั้งฉากกับหน้าจั่ว) โผล่จากปลายสันแล้วโค้งขึ้น/ออกนอกอาคาร", ha="center",
            fontsize=10.5)
    ax.set_xlim(-2.5, 12.5)
    ax.set_ylim(-2.4, 5.8)
    save(f, "05_chofa_types.png")


# ---------------------------------------------------------------- 6. ปั้นลมตามฐานานุศักดิ์
def panlom_rank():
    f, ax = fig(13, 5, "ปั้นลมเปลี่ยนตามฐานานุศักดิ์ (ภาสกร แสงสว่าง, 2560)")
    def jomhae(x0, b, h, n=30, sag=0.12):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = b * (1 - t)
            y = h * t - sag * h * math.sin(math.pi * t)
            pts.append((x0 + x, y))
        return pts
    # เครื่องผูก: straight
    ax.plot([-3, 0, 3], [0, 3.2, 0], color="#7a5a2a", lw=4)
    ax.text(0, -0.9, "เรือนเครื่องผูก\nไม้ตรง ไม่แต่งทรง", ha="center", fontsize=10.5)
    # เครื่องสับ: จอมแห curve, ตัวเหงา foot, หางปลา top
    p = jomhae(8, 3, 3.6)
    ax.plot([q[0] for q in p], [q[1] for q in p], color="#7a5a2a", lw=4)
    ax.plot([2 * 8 - q[0] for q in p], [q[1] for q in p], color="#7a5a2a", lw=4)
    for s in (-1, 1):
        ax.plot([8 + s * 3, 8 + s * 3.4, 8 + s * 3.3], [0, 0.25, 0.6], color="#7a5a2a", lw=4)
    ax.plot([8, 7.7, 8.0, 8.3, 8], [3.6, 4.1, 3.9, 4.1, 3.6], color="#7a5a2a", lw=2)
    ax.text(8, -0.9, "เรือนเครื่องสับ\nเส้นจอมแห ตีนเป็นตัวเหงา ยอดหางปลา", ha="center", fontsize=10.5)
    # ชั้นสูง: รวยระกา + ใบระกา + ช่อฟ้า + หางหงส์
    p = jomhae(16, 3.2, 3.9)
    ax.plot([q[0] for q in p], [q[1] for q in p], color=RED, lw=4)
    ax.plot([2 * 16 - q[0] for q in p], [q[1] for q in p], color=RED, lw=4)
    for q in p[3:-3:3]:
        for s in (1, -1):
            x = q[0] if s > 0 else 2 * 16 - q[0]
            ax.plot([x, x], [q[1] + 0.15, q[1] + 0.55], color=GOLD, lw=2)
    ax.plot([16, 16.1, 16.35, 16.25], [3.9, 4.5, 5.0, 5.3], color=GOLD, lw=3.5)
    for s in (-1, 1):
        ax.plot([16 + s * 3.2, 16 + s * 3.5, 16 + s * 3.6], [0, 0.6, 1.2], color=GOLD, lw=3.5)
    ax.text(16, -0.9, "อาคารทรงไทยชั้นสูง (วัด / วัง)\nรวยระกา ใบระกา ช่อฟ้า หางหงส์", ha="center", fontsize=10.5)
    ax.set_xlim(-4, 20.5)
    ax.set_ylim(-2, 6)
    save(f, "06_panlom_by_rank.png")


# ---------------------------------------------------------------- 7. ยอดบุษบก-มณฑป: ทรงจอมแห proportions (หน้าจั่ว ฉ.12 2558)
def spire_method():
    f, ax = fig(10, 11, "การขึ้นทรงยอดบุษบก–มณฑป ใต้เส้นทรงจอมแห (ชุดเชิงกลอน 5 ชั้น)")
    W, H = 1.0, 2.5                          # ทรงจอมแห: width 1 : height 2.5
    s = 4.0
    n = 60
    curve = []
    for i in range(n + 1):
        t = i / n
        half = (W / 2) * (1 - t) ** 1.9      # concave flank (โค้งแอ่น รวบขึ้น)
        curve.append((half * s, t * H * s))
    xs = [c[0] for c in curve]
    ys = [c[1] for c in curve]
    ax.plot(xs, ys, color=BLUE, lw=1.6)
    ax.plot([-x for x in xs], ys, color=BLUE, lw=1.6)
    roof_h = H * s / 2.5                     # หลังคา 1 ส่วน : ยอด 1.5 ส่วน
    ax.plot([-2.6, 3.2], [roof_h, roof_h], color=GREY, ls="--")
    ax.text(0.95, roof_h - 0.25, "บ่าองค์ระฆัง (หลังคา 1 ส่วน : ยอด 1.5 ส่วน)", fontsize=9.5, va="center")
    # 5 เชิงกลอน sets, heights grow upward (ร.8 model: 0.96 1.08 1.20 1.32, bell 2.05)
    hs = [0.96, 1.08, 1.20, 1.32, 2.05]
    scale = roof_h / sum(hs)
    z = 0.0
    names = ["เชิงกลอน 1", "เชิงกลอน 2", "เชิงกลอน 3", "เชิงกลอน 4", "เชิงกลอน 5 + องค์ระฆัง"]
    for k, hh in enumerate(hs):
        zz = z + hh * scale
        def half_at(y):
            t = y / (H * s)
            return (W / 2) * (1 - t) ** 1.9 * s
        hw = half_at(z)
        ax.add_patch(Rectangle((-hw, z), 2 * hw, (zz - z) * 0.35, fc="#ead7b5", ec=INK, lw=1))
        top = half_at(zz)
        ax.add_patch(MPoly([(-hw * 0.93, z + (zz - z) * 0.35), (hw * 0.93, z + (zz - z) * 0.35), (top, zz), (-top, zz)],
                           closed=True, fc="#d9b98a", ec=INK, lw=1))
        ax.text(-2.75, (z + zz) / 2, f"{names[k]}  {hh:.2f} ม.", fontsize=9, ha="right", va="center")
        z = zz
    ax.text(-2.75, -0.35, "ตัวอย่างพระเมรุมาศ ร.8: ระยะชุดเชิงกลอนเพิ่มทีละ 0.12 ม. ชั้นที่ส่งไปองค์ระฆังเพิ่มพิเศษ", fontsize=9,
            ha="right")
    # spire part
    parts = ["บัวคอเสื้อ + บัลลังก์", "เหม 3 ชั้น", "บัวกลุ่ม (5 ชั้น)", "ปลี", "ลูกแก้ว + บัวคลุ่ม", "ปลียอด", "เม็ดน้ำค้าง"]
    span = H * s - roof_h
    for k, name in enumerate(parts):
        y = roof_h + span * (k + 0.5) / len(parts)
        ax.plot([0.15, 0.9], [y, y], color=GREY, lw=0.8)
        ax.text(0.95, y, name, fontsize=9.5, va="center")
    ax.annotate("", (3.3, 0), (3.3, H * s), arrowprops=dict(arrowstyle="<->", color=BLUE))
    ax.text(3.4, H * s * 0.75, "สูง 2–2.5 ส่วน", color=BLUE, fontsize=10)
    ax.annotate("", (-W / 2 * s, -0.9), (W / 2 * s, -0.9), arrowprops=dict(arrowstyle="<->", color=BLUE))
    ax.text(0, -1.25, "กว้าง 1 ส่วน (ท้องเชิงกลอนชั้นที่ 1)", color=BLUE, ha="center", fontsize=10)
    ax.text(0, -2.1, "เชิงกลอนบนสุดกว้าง ≈ 1/3 ของเชิงกลอนล่างสุด · องค์ระฆังสูง ≈ ความกว้างเชิงกลอนบนสุด\n"
                     "ที่มา: บทความยอดบุษบก-มณฑป วารสารหน้าจั่ว ฉบับที่ 12 (2558)", ha="center", fontsize=9.5)
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-2.6, H * s + 0.6)
    save(f, "07_spire_jomhae_method.png")


# ---------------------------------------------------------------- 8. กนกสามตัว structure
def kranok():
    f, ax = fig(9, 7.5, "โครงสร้างกระหนกสามตัว (แม่ลายของกระหนกทุกชนิด)")
    ax.add_patch(MPoly([(0, 0), (4, 0), (0, 7)], closed=True, fc="none", ec=GREY, ls="--", lw=1.2))
    ax.text(4.2, 0.2, "สามเหลี่ยมมุมฉาก ด้านไม่เท่า\nสูงกว่ากว้าง (หรือทรงดอกบัวครึ่งซีก)", fontsize=9.5, color="#555")
    # ตัวเหงา: lower front, a spiral turned face-down, tip up
    import numpy as np
    th = np.linspace(0, 2.6 * math.pi, 200)
    r = 0.15 + 0.22 * th / (2.6 * math.pi) * 4
    ax.plot(1.5 + r * np.cos(th + math.pi), 1.2 + r * np.sin(th + math.pi) * 0.8, color=RED, lw=2.4)
    ax.plot([2.4, 3.1, 3.3], [1.4, 2.0, 2.9], color=RED, lw=2.4)
    label(ax, 1.5, 1.2, "1. ตัวเหงา: ล่างและหน้าสุด ขมวดก้นหอยคว่ำหน้า ปลายยอดตั้งขึ้น\n   รองรับกาบและตัวยอด (ส่วนที่ 1)", 4.5, 1.2,
          RED, 9.5)
    # กาบ / ตัวประกบหลัง
    ax.plot([0.5, 0.7, 1.4, 2.2, 2.6], [0.6, 2.4, 3.6, 4.0, 3.4], color=BLUE, lw=2.4)
    label(ax, 1.4, 3.6, "2. กาบ / ตัวประกบหลัง: ประกบหลังตัวเหงา ส่งให้เกิดตัวยอด (ส่วนที่ 2)", 4.5, 3.6, BLUE, 9.5)
    # ตัวยอด: flame tip
    ax.plot([0.4, 0.6, 1.0, 0.9, 0.5, 0.2], [3.0, 4.6, 5.8, 6.4, 6.9, 7.3], color=GOLD, lw=2.6)
    label(ax, 0.9, 6.3, "3. ตัวยอด: เปลวบนสุด ปลายสะบัดอ่อนไหวคล้ายเปลวไฟ\n   โคนมีกาบหุ้ม (ส่วนที่ 3)", 4.5, 6.3, GOLD, 9.5)
    ax.text(2, -0.9, "ต้นแบบของกระหนกเปลว กระหนกใบเทศ กระหนกหางโต ฯลฯ — บากตัวลายละเอียดขึ้นก็ยังแบ่งตามโครงนี้\n"
                     "ที่มา: เอกสารประกอบการสอนศิลปะไทย มหาวิทยาลัยราชภัฏสวนสุนันทา บทที่ 9", ha="left", fontsize=9)
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-1.6, 7.8)
    save(f, "08_kranok_sam_tua.png")


# ---------------------------------------------------------------- 9. basic mother patterns (schematic)
def mae_lai():
    f, ax = fig(13, 4.8, "แม่ลายพื้นฐาน (แผนภาพโครงสร้าง ไม่ใช่ลายจริง)")
    # กระจังฟันปลา: triangle in a square
    ax.add_patch(Rectangle((0, 0), 2, 2, fc="none", ec=GREY, ls="--"))
    ax.add_patch(MPoly([(0, 0), (2, 0), (1, 2)], closed=True, fc="#e7c98f", ec=INK))
    ax.text(1, -0.6, "กระจังฟันปลา\nสามเหลี่ยมในสี่เหลี่ยม", ha="center", fontsize=9.5)
    # กระจังตาอ้อย: curved sides, notched tip
    pts = [(3.2, 0), (5.2, 0), (4.9, 0.8), (4.4, 1.5), (4.35, 1.75), (4.2, 1.6), (4.25, 2.2), (4.15, 1.6), (4.0, 1.75),
           (3.95, 1.5), (3.5, 0.8)]
    ax.add_patch(MPoly(pts, closed=True, fc="#e7c98f", ec=INK))
    ax.text(4.2, -0.6, "กระจังตาอ้อย\nข้างอ่อนเรียว ปลายบาก", ha="center", fontsize=9.5)
    # กระจังใบเทศ: layered inner divisions (แข้งสิงห์)
    ax.add_patch(MPoly([(6.4, 0), (8.4, 0), (7.4, 2.4)], closed=True, fc="#e7c98f", ec=INK))
    ax.add_patch(MPoly([(6.8, 0.2), (8.0, 0.2), (7.4, 1.7)], closed=True, fc="none", ec=RED))
    ax.add_patch(MPoly([(7.1, 0.35), (7.7, 0.35), (7.4, 1.1)], closed=True, fc="none", ec=RED))
    ax.text(7.4, -0.6, "กระจังใบเทศ\nแบ่งชั้นใน (แข้งสิงห์)", ha="center", fontsize=9.5)
    # ประจำยาม: diagonal square + circle + 4 petals
    cx, cy = 10.4, 1.0
    ax.add_patch(MPoly([(cx, cy - 1.1), (cx + 1.1, cy), (cx, cy + 1.1), (cx - 1.1, cy)], closed=True, fc="#e7c98f", ec=INK))
    for a in range(4):
        t = math.radians(90 * a)
        ax.add_patch(Circle((cx + 0.5 * math.cos(t), cy + 0.5 * math.sin(t)), 0.28, fc="none", ec=RED))
    ax.add_patch(Circle((cx, cy), 0.22, fc=RED))
    ax.text(cx, -0.6, "ประจำยาม\nสี่เหลี่ยมตะแคง ดอกสี่ทิศ", ha="center", fontsize=9.5)
    # พุ่มข้าวบิณฑ์ 2:3
    x0 = 12.4
    ax.add_patch(Rectangle((x0, 0), 2, 3, fc="none", ec=GREY, ls="--"))
    ax.add_patch(MPoly([(x0 + 0.2, 0.2), (x0 + 1.8, 0.2), (x0 + 1.0, 1.5)], closed=True, fc="#e7c98f", ec=INK))
    ax.add_patch(MPoly([(x0 + 0.2, 1.5), (x0 + 1.8, 1.5), (x0 + 1.0, 3.0)], closed=True, fc="#e7c98f", ec=INK))
    ax.text(x0 + 1, -0.6, "พุ่มข้าวบิณฑ์\nกว้าง 2 : สูง 3 กระจังใบเทศ 2 ตัวต่อกัน", ha="center", fontsize=9.5)
    ax.set_xlim(-0.5, 15)
    ax.set_ylim(-1.4, 3.4)
    save(f, "09_mae_lai_basic.png")


# ---------------------------------------------------------------- 10. ย่อมุม plans
def redent_plans():
    f, ax = fig(13, 4, "ย่อมุม: นับจำนวนมุมนอก")
    def redent(cx, w, s, n):
        from shapely.geometry import box
        from shapely.ops import unary_union
        g = box(-w, -w, w, w) if n == 0 else unary_union([box(-(w - k * s), -(w - (n - k) * s), w - k * s, w - (n - k) * s)
                                                          for k in range(n + 1)])
        xs, ys = g.exterior.xy
        ax.add_patch(MPoly([(cx + x, y) for x, y in zip(xs, ys)], closed=True, fc="#ead7b5", ec=INK))
    for i, (n, name) in enumerate([(0, "ไม้สี่ (ไม่ย่อ)"), (1, "ย่อมุมไม้แปด"), (2, "ย่อมุมไม้สิบสอง"), (4, "ย่อมุมไม้ยี่สิบ")]):
        redent(i * 3.2, 1.2, 0.22, n)
        ax.text(i * 3.2, -1.7, name, ha="center", fontsize=10.5)
    ax.set_xlim(-1.6, 11.3)
    ax.set_ylim(-2.1, 1.5)
    save(f, "10_yo_mum_plans.png")


# ---------------------------------------------------------------- 11. Wat Arun plan = Traiphum
def wat_arun_plan():
    f, ax = fig(8, 8, "ผังหมู่พระปรางค์วัดอรุณ: จำลองจักรวาลตามคติไตรภูมิ")
    for r, c in [(9, "#f2efe8"), (7, "#e9e3d6"), (5, "#ded4bf")]:
        ax.add_patch(Rectangle((-r, -r), 2 * r, 2 * r, fc=c, ec=GREY))
    ax.add_patch(Circle((0, 0), 2.6, fc="#d8b77a", ec=INK))
    ax.text(0, 0, "ปรางค์ประธาน\n= เขาพระสุเมรุ\nยอดมีมงกุฎ (คติพระอินทร์)", ha="center", va="center", fontsize=9.5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax.add_patch(Circle((sx * 7.2, sy * 7.2), 1.0, fc="#e0c48e", ec=INK))
    ax.text(7.2, 8.6, "ปรางค์ทิศ (มุม)", ha="center", fontsize=9.5)
    for nx, ny in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        ax.add_patch(Rectangle((nx * 7.2 - (0.9 if nx == 0 else 0.6), ny * 7.2 - (0.6 if nx == 0 else 0.9)),
                               1.8 if nx == 0 else 1.2, 1.2 if nx == 0 else 1.8, fc="#c9b38a", ec=INK))
    ax.text(0, 8.6, "มณฑปทิศ (แกน 4 ทิศ)", ha="center", fontsize=9.5)
    ax.text(0, -10.2, "ฐานซ้อนเป็นชั้นรอบองค์ = เขาสัตตบริภัณฑ์ล้อมเขาพระสุเมรุ (แผนภาพแนวคิด ไม่ใช่ผังจริง)", ha="center",
            fontsize=9.5)
    ax.set_xlim(-10.5, 10.5)
    ax.set_ylim(-11, 10)
    save(f, "11_wat_arun_cosmology_plan.png")


# ---------------------------------------------------------------- 12. ฐาน profiles (schematic sections)
def base_profiles():
    f, ax = fig(13, 5.2, "ฐาน: รูปตัดด้านข้างแบบแผนภาพ (ซ้าย = ด้านนอก)")
    def prof(x0, pts, name):
        pts = [(x0 + x, y) for x, y in pts]
        ax.add_patch(MPoly(pts + [(x0 + 2.2, pts[-1][1]), (x0 + 2.2, 0)], closed=True, fc="#ead7b5", ec=INK))
        ax.text(x0 + 1.0, -0.6, name, ha="center", fontsize=10)
    prof(0, [(0, 0), (0, 0.6), (0.3, 0.6), (0.3, 1.2), (0.6, 1.2), (0.6, 1.8)], "ฐานเขียง")
    prof(3.2, [(0, 0), (0, 0.4), (0.05, 0.45), (0.35, 0.9), (0.55, 0.95), (0.55, 1.45), (0.35, 1.5), (0.05, 1.95),
               (0, 2.0), (0, 2.4)], "ฐานบัว (บัวคว่ำ ท้องไม้ บัวหงาย)")
    prof(6.4, [(0, 0), (0, 0.4), (0.35, 0.9), (0.55, 0.95), (0.4, 1.1), (0.4, 1.3), (0.55, 1.45), (0.35, 1.5),
               (0, 2.0), (0, 2.4)], "ฐานบัวลูกแก้ว (ลูกแก้วกลางท้องไม้)")
    prof(9.6, [(0, 0), (0, 0.35), (-0.15, 0.45), (0.25, 0.75), (0.15, 1.05), (0.4, 1.2), (0.55, 1.25), (0.55, 1.6),
               (0.35, 1.65), (0.05, 2.05), (0, 2.45)], "ฐานสิงห์ (เท้าสิงห์เตะออก)")
    ax.text(6.5, -1.4, "แผนภาพเพื่อจำลำดับชั้นเท่านั้น สัดส่วนจริงต่างกันตามยุคและช่าง", ha="center", fontsize=9.5, color="#555")
    ax.set_xlim(-0.6, 12.4)
    ax.set_ylim(-1.8, 2.8)
    save(f, "12_base_profiles.png")


if __name__ == "__main__":
    for fn in (son, son_section, lot, lamyong, chofa_types, panlom_rank, spire_method, kranok, mae_lai, redent_plans,
               wat_arun_plan, base_profiles):
        fn()
