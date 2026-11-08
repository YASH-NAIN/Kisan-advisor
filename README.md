# Crop Disease & Agronomic Advisory Expert System (AI Foundations, Group 4)

Hybrid project: rule-based expert system (frames + production rules) + ML leaf-image classifier.

## Run (3 commands)
    pip install -r requirements.txt
    streamlit run app.py
(The trained model is already in models/. To retrain: `python train_model.py`)

## Folders / files
- dataset/        PlantVillage subset: 8 classes x 500 images (tomato, potato, maize)
- features.py     image features (HSV colour histograms, texture, spatial colour grid)
- train_model.py  trains Random Forest, prints accuracy + confusion matrix
- models/         trained model
- knowledge_base.py  FRAMES (problem, treatment, prevention in English/Hindi) + RULES
- engine.py       forward-chaining inference, certainty factors, explanation trace
- app.py          Streamlit front end

## How it works
1. User enters crop, growth stage, soil, weather, irrigation, symptoms (+ optional leaf photo).
2. Rules fire (forward chaining) -> candidate problems with confidence.
3. Image model prediction (only if confidence >= 60%) is combined using certainty factors: cf = a + b(1-a).
4. Output: diagnosis, treatment, prevention, and a "Why?" trace of matched conditions, in English/Hindi.

## Results
Random Forest on 8 classes: ~95% test accuracy (see train_model.py output).
Weak spot: Tomato early vs late blight get confused (visually similar) - mention in report.

## Report ideas
- Compare rules only vs image only vs combined.
- Limitations: PlantVillage = clean lab photos; real field photos will do worse.
- Future work: CNN transfer learning (MobileNetV2), Punjabi language, more crops/rules.

Dataset: PlantVillage (Hughes & Salathe, 2015), github.com/spMohanty/PlantVillage-Dataset

## Knowledge representation (v2)
- **Frames:** `knowledge_base.py` defines an is-a hierarchy: Problem > Disease > FungalDisease / BacterialDisease, Problem > Pest, Problem > NutrientDeficiency, Problem > AbioticStress. 12 instance frames (late blight, early blight, rust, powdery mildew, rice blast, bacterial leaf spot, aphids, stem borer, nitrogen deficiency, potassium deficiency, water stress, root rot) inherit missing slots (treatment, prevention, kind, note) from their parents.
- **Slots:** name (en/hi), affects (crops), favourable (weather), treatment, prevention.
- **Rules:** 12 production rules with certainty factors, using crop, stage, soil, weather, irrigation and symptoms.
- **Inference:** forward chaining; a frame check drops problems that do not affect the crop and adds a weather bonus; an optional image model adds evidence by certainty-factor combination.
- **Tests:** `python tests.py` runs 13 sample cases.
