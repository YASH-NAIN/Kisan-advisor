"""Knowledge base: FRAME hierarchy (is-a, slots, inheritance) + production RULES.
Slots with {en, hi} values are multilingual. Instances inherit missing slots from parents."""

def L(en, hi): return {"en": en, "hi": hi}

FRAMES = {
 # ---------- class frames (abstract) ----------
 "Problem": {"is_a": None, "affects": "any", "favourable": [],
             "note": L("Follow product label dose. Confirm serious cases with an agriculture officer.",
                       "दवा के लेबल की मात्रा का पालन करें। गंभीर मामलों में कृषि अधिकारी से पुष्टि करें।")},
 "Disease": {"is_a": "Problem", "kind": "disease",
             "prevention": L("Remove infected plant debris, rotate crops, use certified disease-free seed.",
                             "संक्रमित अवशेष हटाएँ, फसल चक्र अपनाएँ, प्रमाणित रोगमुक्त बीज लगाएँ।")},
 "FungalDisease": {"is_a": "Disease", "treatment": L("Spray a recommended fungicide at first sign and repeat after 7-10 days.",
                                                      "शुरुआती लक्षण पर अनुशंसित फफूंदनाशी छिड़कें और 7-10 दिन बाद दोहराएँ।")},
 "BacterialDisease": {"is_a": "Disease", "treatment": L("Spray copper-based bactericide; avoid working in wet fields.",
                                                        "कॉपर आधारित जीवाणुनाशी छिड़कें; गीले खेत में काम न करें।")},
 "Pest": {"is_a": "Problem", "kind": "pest",
          "prevention": L("Scout weekly, use traps and encourage natural enemies.",
                          "साप्ताहिक निरीक्षण करें, ट्रैप लगाएँ और मित्र कीटों को बढ़ावा दें।")},
 "NutrientDeficiency": {"is_a": "Problem", "kind": "nutrient",
          "prevention": L("Test soil every season and apply balanced fertilizer with organic manure.",
                          "हर मौसम मिट्टी जाँच कराएँ और जैविक खाद के साथ संतुलित उर्वरक दें।")},
 "AbioticStress": {"is_a": "Problem", "kind": "water"},

 # ---------- instance frames (the 12 problems) ----------
 "late_blight": {"is_a": "FungalDisease", "affects": ["tomato", "potato"], "favourable": ["humid_cool", "rainy"],
   "name": L("Late Blight", "पछेती झुलसा"),
   "treatment": L("Spray mancozeb (or mancozeb + metalaxyl); destroy badly infected plants.",
                  "मैन्कोज़ेब (या मैन्कोज़ेब + मेटालैक्सिल) छिड़कें; अत्यधिक संक्रमित पौधे नष्ट करें।"),
   "prevention": L("Use resistant varieties, avoid overhead irrigation, keep proper spacing.",
                   "प्रतिरोधी किस्में लगाएँ, ऊपर से सिंचाई न करें, उचित दूरी रखें।")},
 "early_blight": {"is_a": "FungalDisease", "affects": ["tomato", "potato"], "favourable": ["rainy", "normal"],
   "name": L("Early Blight", "अगेती झुलसा"),
   "treatment": L("Apply chlorothalonil or mancozeb; remove lower infected leaves.",
                  "क्लोरोथालोनिल या मैन्कोज़ेब लगाएँ; निचली संक्रमित पत्तियाँ हटाएँ।"),
   "prevention": L("Rotate crops, mulch the soil, avoid wetting leaves, keep plants well fed.",
                   "फसल चक्र अपनाएँ, मल्चिंग करें, पत्तियाँ गीली न करें, पौधों को पोषण दें।")},
 "rust": {"is_a": "FungalDisease", "affects": ["wheat", "maize"], "favourable": ["humid_cool", "rainy"],
   "name": L("Rust", "रतुआ"),
   "treatment": L("Spray propiconazole or tebuconazole at first sign.",
                  "शुरुआती लक्षण पर प्रोपिकोनाज़ोल या टेबुकोनाज़ोल छिड़कें।"),
   "prevention": L("Grow resistant varieties and sow on time.", "प्रतिरोधी किस्में उगाएँ और समय पर बुवाई करें।")},
 "powdery_mildew": {"is_a": "FungalDisease", "affects": ["tomato", "wheat", "potato"], "favourable": ["hot_dry", "normal"],
   "name": L("Powdery Mildew", "चूर्णिल आसिता (पाउडरी मिल्ड्यू)"),
   "treatment": L("Spray wettable sulphur or hexaconazole.", "घुलनशील गंधक या हेक्साकोनाज़ोल छिड़कें।"),
   "prevention": L("Ensure air circulation; avoid excess nitrogen.", "हवा का संचार रखें; अधिक नाइट्रोजन न दें।")},
 "rice_blast": {"is_a": "FungalDisease", "affects": ["rice"], "favourable": ["humid_cool", "rainy"],
   "name": L("Rice Blast", "धान का झोंका रोग (ब्लास्ट)"),
   "treatment": L("Spray tricyclazole as per label.", "लेबल के अनुसार ट्राइसाइक्लाज़ोल छिड़कें।"),
   "prevention": L("Use resistant varieties and split nitrogen doses.", "प्रतिरोधी किस्में लगाएँ और नाइट्रोजन कई बार में दें।")},
 "bacterial_leaf_spot": {"is_a": "BacterialDisease", "affects": ["tomato"], "favourable": ["rainy"],
   "name": L("Bacterial Leaf Spot", "जीवाणु पत्ती धब्बा"),
   "prevention": L("Use clean seed, avoid overhead irrigation, rotate with non-host crops.",
                   "स्वच्छ बीज लें, ऊपर से सिंचाई न करें, अन्य फसल के साथ चक्र अपनाएँ।")},
 "aphids": {"is_a": "Pest", "affects": "any", "favourable": ["hot_dry", "normal"],
   "name": L("Aphid Infestation", "माहू (एफिड) प्रकोप"),
   "treatment": L("Spray neem oil (5 ml/L); use imidacloprid only if severe.",
                  "नीम तेल (5 मिली/लीटर) छिड़कें; गंभीर होने पर ही इमिडाक्लोप्रिड।")},
 "stem_borer": {"is_a": "Pest", "affects": ["maize", "rice"], "favourable": ["normal", "rainy"],
   "name": L("Stem Borer", "तना छेदक कीट"),
   "treatment": L("Apply chlorantraniliprole granules in the whorl as per label; remove dead hearts.",
                  "लेबल के अनुसार क्लोरेंट्रानिलिप्रोल दाने पोटली में डालें; सूखे गुच्छे हटाएँ।"),
   "prevention": L("Destroy stubble after harvest and install pheromone traps.",
                   "कटाई के बाद ठूँठ नष्ट करें और फेरोमोन ट्रैप लगाएँ।")},
 "nitrogen_deficiency": {"is_a": "NutrientDeficiency", "affects": "any", "favourable": [],
   "name": L("Nitrogen Deficiency", "नाइट्रोजन की कमी"),
   "treatment": L("Top-dress with urea or apply well-rotted compost.", "यूरिया की टॉप ड्रेसिंग करें या सड़ी खाद डालें।")},
 "potassium_deficiency": {"is_a": "NutrientDeficiency", "affects": "any", "favourable": [],
   "name": L("Potassium Deficiency", "पोटैशियम की कमी"),
   "treatment": L("Apply muriate of potash (MOP) based on soil test.", "मिट्टी जाँच के आधार पर म्यूरेट ऑफ पोटाश (MOP) दें।")},
 "water_stress": {"is_a": "AbioticStress", "affects": "any", "favourable": ["hot_dry"],
   "name": L("Water Stress", "जल तनाव"),
   "treatment": L("Irrigate immediately, preferably early morning.", "तुरंत सिंचाई करें, सुबह जल्दी बेहतर है।"),
   "prevention": L("Use mulching and drip irrigation.", "मल्चिंग और ड्रिप सिंचाई अपनाएँ।")},
 "root_rot": {"is_a": "AbioticStress", "affects": "any", "favourable": ["rainy"],
   "name": L("Root Rot (waterlogging)", "जड़ सड़न (जलभराव)"),
   "treatment": L("Stop irrigation, improve drainage, apply Trichoderma to the soil.",
                  "सिंचाई रोकें, जल निकास सुधारें, मिट्टी में ट्राइकोडर्मा डालें।"),
   "prevention": L("Use raised beds and ensure proper drainage.", "ऊँची क्यारियाँ बनाएँ और जल निकास रखें।")},
}

# RULES: (field, allowed_values, required). cf = rule certainty factor.
RULES = [
 {"id": "R1", "problem": "late_blight", "cf": 0.85, "conds": [
   ("crop", {"tomato", "potato"}, True), ("symptoms", {"dark_water_soaked_spots"}, True),
   ("weather", {"humid_cool", "rainy"}, False)]},
 {"id": "R2", "problem": "early_blight", "cf": 0.80, "conds": [
   ("crop", {"tomato", "potato"}, True), ("symptoms", {"concentric_ring_spots"}, True),
   ("stage", {"vegetative", "flowering", "fruiting"}, False), ("soil", {"low_nitrogen"}, False)]},
 {"id": "R3", "problem": "rust", "cf": 0.80, "conds": [
   ("crop", {"wheat", "maize"}, True), ("symptoms", {"orange_pustules"}, True),
   ("weather", {"humid_cool", "rainy"}, False), ("stage", {"vegetative", "flowering"}, False)]},
 {"id": "R4", "problem": "powdery_mildew", "cf": 0.80, "conds": [
   ("crop", {"tomato", "wheat", "potato"}, True), ("symptoms", {"white_powdery_coating"}, True),
   ("weather", {"hot_dry", "normal"}, False)]},
 {"id": "R5", "problem": "bacterial_leaf_spot", "cf": 0.75, "conds": [
   ("crop", {"tomato"}, True), ("symptoms", {"small_angular_water_spots"}, True),
   ("weather", {"rainy"}, False), ("irrigation", {"excess"}, False)]},
 {"id": "R6", "problem": "rice_blast", "cf": 0.85, "conds": [
   ("crop", {"rice"}, True), ("symptoms", {"diamond_shaped_lesions"}, True),
   ("weather", {"humid_cool", "rainy"}, False), ("stage", {"seedling", "vegetative"}, False)]},
 {"id": "R7", "problem": "aphids", "cf": 0.80, "conds": [
   ("symptoms", {"curled_leaves", "sticky_honeydew"}, True),
   ("weather", {"hot_dry", "normal"}, False), ("stage", {"seedling", "vegetative", "flowering"}, False)]},
 {"id": "R8", "problem": "stem_borer", "cf": 0.80, "conds": [
   ("crop", {"maize", "rice"}, True), ("symptoms", {"dead_heart_or_stem_holes"}, True),
   ("stage", {"vegetative"}, False)]},
 {"id": "R9", "problem": "nitrogen_deficiency", "cf": 0.75, "conds": [
   ("symptoms", {"yellowing_lower_leaves"}, True), ("soil", {"low_nitrogen"}, False),
   ("symptoms", {"stunted_growth"}, False), ("stage", {"vegetative", "flowering"}, False)]},
 {"id": "R10", "problem": "potassium_deficiency", "cf": 0.75, "conds": [
   ("symptoms", {"leaf_margin_browning"}, True), ("soil", {"low_potassium"}, False),
   ("stage", {"flowering", "fruiting"}, False)]},
 {"id": "R11", "problem": "water_stress", "cf": 0.80, "conds": [
   ("symptoms", {"wilting"}, True), ("irrigation", {"scarce"}, False),
   ("soil", {"dry"}, False), ("weather", {"hot_dry"}, False)]},
 {"id": "R12", "problem": "root_rot", "cf": 0.80, "conds": [
   ("symptoms", {"wilting"}, True), ("soil", {"waterlogged"}, False),
   ("irrigation", {"excess"}, False), ("symptoms", {"root_darkening"}, False)]},
]

OPTIONS = {
  "crop": ["tomato", "potato", "wheat", "maize", "rice"],
  "stage": ["seedling", "vegetative", "flowering", "fruiting"],
  "soil": ["normal", "low_nitrogen", "low_potassium", "dry", "waterlogged"],
  "weather": ["normal", "humid_cool", "rainy", "hot_dry"],
  "irrigation": ["adequate", "scarce", "excess"],
  "symptoms": ["dark_water_soaked_spots", "concentric_ring_spots", "orange_pustules", "white_powdery_coating",
               "small_angular_water_spots", "diamond_shaped_lesions", "yellowing_lower_leaves", "stunted_growth",
               "leaf_margin_browning", "wilting", "root_darkening", "curled_leaves", "sticky_honeydew",
               "dead_heart_or_stem_holes"],
}

# Map image-model class names -> problem frames
CNN_TO_PROBLEM = {
  "Tomato___Late_blight": "late_blight", "Potato___Late_blight": "late_blight",
  "Tomato___Early_blight": "early_blight", "Potato___Early_blight": "early_blight",
  "Corn_(maize)___Common_rust_": "rust",
}
