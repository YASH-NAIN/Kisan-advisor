"""Forward-chaining inference engine + frame inheritance + explanations."""
from knowledge_base import RULES, FRAMES, CNN_TO_PROBLEM

def get_slot(frame, slot):
    """Frame inheritance: walk up the is-a chain until the slot is found."""
    while frame:
        f = FRAMES[frame]
        if slot in f:
            return f[slot]
        frame = f["is_a"]
    return None

def chain(frame):
    out = []
    while frame:
        out.append(frame); frame = FRAMES[frame]["is_a"]
    return out

def _match(field, allowed, facts):
    v = facts.get(field)
    if isinstance(v, (list, set)):
        return bool(set(v) & allowed)
    return v in allowed

def infer(facts, cnn=None):
    """facts: dict of observations. cnn: optional (class_name, prob) from the image model."""
    results = {}
    for r in RULES:
        trace, ok, matched = [], True, 0
        for field, allowed, req in r["conds"]:
            if _match(field, allowed, facts):
                matched += 1
                trace.append(f"RULE {r['id']}: {field} = {facts.get(field)} matches {sorted(allowed)}")
            elif req:
                ok = False
                break
        if not ok:
            continue
        conf = r["cf"] * matched / len(r["conds"])
        prob = r["problem"]
        # --- frame knowledge check (uses slots + inheritance) ---
        affects = get_slot(prob, "affects")
        if affects != "any" and facts.get("crop") not in affects:
            continue
        fav = get_slot(prob, "favourable") or []
        if facts.get("weather") in fav:
            conf += 0.05
            trace.append(f"FRAME {prob}: weather '{facts.get('weather')}' is favourable for this problem (+0.05)")
        trace.append("FRAME chain: " + " is-a ".join(chain(prob)))
        results[prob] = {"rule": r["id"], "confidence": round(min(conf, 0.99), 2), "trace": trace}
    if cnn:
        cls, p = cnn
        prob = CNN_TO_PROBLEM.get(cls)
        if prob:
            e = results.setdefault(prob, {"rule": "CNN", "confidence": 0.0, "trace": []})
            e["trace"].append(f"IMAGE MODEL predicted '{cls}' ({p:.0%})")
            e["confidence"] = round(e["confidence"] + p * (1 - e["confidence"]), 2)  # CF combination
    return sorted(results.items(), key=lambda kv: -kv[1]["confidence"])

def advice(problem, lang="en"):
    g = lambda s: get_slot(problem, s)[lang]
    return g("name"), get_slot(problem, "kind"), g("treatment"), g("prevention")
