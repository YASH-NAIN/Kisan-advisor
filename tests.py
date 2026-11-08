"""Run: python tests.py  -> checks the expert system on sample cases."""
from engine import infer, chain
B = dict(crop="tomato", stage="vegetative", soil="normal", weather="normal", irrigation="adequate", symptoms=[])
CASES = [
 ("Tomato late blight", dict(B, weather="rainy", symptoms=["dark_water_soaked_spots"]), "late_blight"),
 ("Potato early blight", dict(B, crop="potato", symptoms=["concentric_ring_spots"], soil="low_nitrogen"), "early_blight"),
 ("Wheat rust", dict(B, crop="wheat", weather="humid_cool", symptoms=["orange_pustules"]), "rust"),
 ("Tomato powdery mildew", dict(B, weather="hot_dry", symptoms=["white_powdery_coating"]), "powdery_mildew"),
 ("Tomato bacterial spot", dict(B, weather="rainy", irrigation="excess", symptoms=["small_angular_water_spots"]), "bacterial_leaf_spot"),
 ("Rice blast", dict(B, crop="rice", weather="humid_cool", symptoms=["diamond_shaped_lesions"]), "rice_blast"),
 ("Aphids on wheat", dict(B, crop="wheat", symptoms=["curled_leaves", "sticky_honeydew"]), "aphids"),
 ("Maize stem borer", dict(B, crop="maize", symptoms=["dead_heart_or_stem_holes"]), "stem_borer"),
 ("Nitrogen deficiency", dict(B, crop="maize", soil="low_nitrogen", symptoms=["yellowing_lower_leaves", "stunted_growth"]), "nitrogen_deficiency"),
 ("Potassium deficiency", dict(B, stage="fruiting", soil="low_potassium", symptoms=["leaf_margin_browning"]), "potassium_deficiency"),
 ("Water stress", dict(B, soil="dry", irrigation="scarce", weather="hot_dry", symptoms=["wilting"]), "water_stress"),
 ("Root rot", dict(B, soil="waterlogged", irrigation="excess", symptoms=["wilting", "root_darkening"]), "root_rot"),
 ("Rust must NOT fire on rice", dict(B, crop="rice", symptoms=["orange_pustules"]), None),
]
ok = 0
for name, facts, want in CASES:
    res = infer(facts)
    got = res[0][0] if res else None
    good = got == want; ok += good
    print(("PASS" if good else "FAIL"), "-", name, "->", got, (res[0][1]["confidence"] if res else ""))
print(f"\n{ok}/{len(CASES)} passed")
print("Frame chain example:", " -> ".join(chain("late_blight")))
