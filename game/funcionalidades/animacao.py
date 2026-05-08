def update_enemies(enemies):
    for enemy in enemies:
        enemy["x"] += enemy["dir"] * enemy["speed"]
        if enemy["x"] <= enemy["min_x"] or enemy["x"] >= enemy["max_x"]:
            enemy["dir"] *= -1
            enemy["x"] = max(enemy["min_x"], min(enemy["x"], enemy["max_x"]))


def update_platforms(platforms):
    for p in platforms:
        if p["type"] == "move":
            p["_prev_x"] = p["x"]
            p["x"] += p.get("speed", 2) * p["dir"]
            if p["x"] > p.get("max_x", p["x"]) or p["x"] < p.get("min_x", p["x"]):
                p["dir"] *= -1
                p["x"] = max(p.get("min_x", p["x"]), min(p["x"], p.get("max_x", p["x"])))

        elif p["type"] == "scale":
            if p["growing"]:
                p["scale"] += 0.01
                if p["scale"] >= 1.5:
                    p["growing"] = False
            else:
                p["scale"] -= 0.01
                if p["scale"] <= 0.5:
                    p["growing"] = True

            p["w"] = 100 * p["scale"]

        elif p["type"] == "rotate":
            p["angle"] += 1
