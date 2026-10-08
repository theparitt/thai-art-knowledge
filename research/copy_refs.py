"""Copy the reference photos the owner sent during the Wat Arun mondop work into images/reference/ as JPEG
(max 1600 px). Internal reference only: many are third-party photos (watermarks kept), do not publish."""
from pathlib import Path

from PIL import Image

SRC = Path("/mnt/c/Users/User/AppData/Local/Temp/claude/e--work/e1bc5d93-e93e-4156-a157-94fbe7e8af7d/images")
DST = Path(__file__).resolve().parent.parent / "images" / "reference"
DST.mkdir(parents=True, exist_ok=True)
NAMES = {
    14: "wat_arun_mondop_long_face_porch_and_wings",
    16: "wat_arun_mondop_side_with_stairs",
    19: "thai_roof_side_tiers_and_chofa",
    22: "scan_chofa_curve",
    23: "scan_mondop_wing_roof_with_chofa",
    24: "scan_mondop_corner",
    25: "scan_mondop_base_follows_porch",
    26: "scan_mondop_front_gables_and_spire",
    27: "scan_mondop_corner_spire",
    28: "scan_mondop_top_view",
    29: "scan_mondop_crown_gables",
    30: "wat_arun_mondop_west_full_photo",
    31: "phra_mondop_wat_phra_kaew_prasat_roof",
    33: "WRONG_model_v13_rear_gable_narrower",
    34: "wat_arun_mondop_gable_layers",
    35: "grand_palace_son_roofs_parallel_bargeboards",
    36: "son_gables_two_chofa",
    37: "grand_palace_son_gables_three_layers",
    38: "son_three_layers_tile_panels",
    39: "prasat_crossing_garuda_and_spire_tiers",
    40: "dusit_maha_prasat_front_son_gables",
    41: "wat_pho_roof_lot_and_son_side",
    42: "lamyong_detail_bai_raka_ngouang_aiyara",
    43: "son_lot_gables_and_naga_heads",
}
for k, name in NAMES.items():
    im = Image.open(SRC / f"{k}.png").convert("RGB")
    im.thumbnail((1600, 1600))
    im.save(DST / f"{k:02d}_{name}.jpg", quality=86)
    print(k, name, im.size)
