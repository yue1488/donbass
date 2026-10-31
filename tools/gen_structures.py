"""Builds all structure templates (.nbt) and the worldgen JSON that places them:
template pools, jigsaw structures and structure sets."""
import os
import shutil

import structures_industry
import structures_mines
import structures_town
from gen_worldgen import DATA, WG, wj

N = "donbass:"
NBT_DIR = os.path.join(DATA, "structures")


def element(name, processors, weight=1):
    return {"weight": weight, "element": {
        "element_type": "minecraft:single_pool_element", "location": N + name,
        "processors": N + processors if processors else {"processors": []}, "projection": "rigid"}}


def pool(path, elements, fallback="minecraft:empty"):
    wj(os.path.join(WG, "template_pool", path + ".json"), {"fallback": fallback, "elements": elements})


def jigsaw_structure(name, start_pool, size, ground, max_dist, adaptation="beard_thin"):
    wj(os.path.join(WG, "structure", name + ".json"), {
        "type": "minecraft:jigsaw", "biomes": "#donbass:has_structures", "step": "surface_structures",
        "start_pool": N + start_pool, "size": size, "max_distance_from_center": max_dist,
        "start_height": {"absolute": -ground}, "project_start_to_heightmap": "WORLD_SURFACE_WG",
        "use_expansion_hack": False, "terrain_adaptation": adaptation, "spawn_overrides": {}})


def structure_set(name, salt, spacing, separation, structures, exclusion=None):
    placement = {"type": "minecraft:random_spread", "salt": salt, "spacing": spacing, "separation": separation}
    if exclusion:
        placement["exclusion_zone"] = {"other_set": N + exclusion[0], "chunk_count": exclusion[1]}
    wj(os.path.join(WG, "structure_set", name + ".json"), {
        "placement": placement,
        "structures": [{"structure": N + s, "weight": w} for s, w in structures]})


def main():
    shutil.rmtree(NBT_DIR, ignore_errors=True)
    for sub in ("template_pool", "structure", "structure_set"):
        shutil.rmtree(os.path.join(WG, sub), ignore_errors=True)

    templates = {}
    templates.update(structures_mines.all_templates())
    town, plot_weights = structures_town.all_templates()
    templates.update(town)
    templates.update(structures_industry.all_templates())

    for name, (tpl, ground) in templates.items():
        for (x, y, z) in tpl.blocks:
            sx, sy, sz = tpl.size
            assert 0 <= x < sx and 0 <= y < sy and 0 <= z < sz, f"{name}: block {(x, y, z)} outside {tpl.size}"
        tpl.save(os.path.join(NBT_DIR, name + ".nbt"))
    grounds = {n: g for n, (_, g) in templates.items()}

    # ---- mines: one single-piece structure each, buried so that the yard lands on the surface
    for kind, proc in (("shallow", "abandoned"), ("active", "weathered"), ("deep", "abandoned")):
        pool("mine/" + kind, [element("mine/" + kind, proc)])
        jigsaw_structure(kind + "_mine", "mine/" + kind, 1, grounds["mine/" + kind], 32, "none")

    # ---- worker settlement
    pool("settlement/centers", [element("settlement/center_monument", "weathered"),
                                element("settlement/center_water_tower", "weathered")])
    pool("settlement/plots", [element(n, "weathered", plot_weights[n]) for n in sorted(plot_weights)])
    jigsaw_structure("miners_settlement", "settlement/centers", 5, 1, 80)

    # ---- industry: each plant exists in a working and in a ruined version
    for plant in ("steelworks", "coke_plant"):
        pool("industry/" + plant, [element("industry/" + plant, "weathered", 2),
                                   element("industry/" + plant, "ruined", 3)])
        jigsaw_structure(plant, "industry/" + plant, 1, 1, 48)

    # ---- railway: station + branch line made of chained track segments, capped by buffer ends
    pool("rail/stations", [element("rail/freight_station", "weathered", 1),
                           element("rail/freight_station", "ruined", 1)])
    pool("rail/line", [element("rail/line_plain", "weathered", 4), element("rail/line_signal", "weathered", 2),
                       element("rail/line_wreck", "ruined", 1), element("rail/line_crossing", "weathered", 2)],
         fallback=N + "rail/ends")
    pool("rail/ends", [element("rail/line_end", "weathered")])
    jigsaw_structure("freight_station", "rail/stations", 5, 1, 96)

    # ---- structure sets (spacing / separation are in chunks)
    structure_set("miners_settlements", 1730101, 16, 6, [("miners_settlement", 1)])
    structure_set("shallow_mines", 1730102, 10, 4, [("shallow_mine", 1)])
    structure_set("active_mines", 1730103, 20, 7, [("active_mine", 1)], exclusion=("miners_settlements", 3))
    structure_set("deep_mines", 1730104, 24, 8, [("deep_mine", 1)], exclusion=("miners_settlements", 3))
    structure_set("industrial_plants", 1730105, 18, 6, [("steelworks", 1), ("coke_plant", 1)],
                  exclusion=("miners_settlements", 4))
    structure_set("freight_stations", 1730106, 22, 7, [("freight_station", 1)], exclusion=("miners_settlements", 4))

    print(f"structures: {len(templates)} templates written to {os.path.relpath(NBT_DIR, DATA)}")


if __name__ == "__main__":
    main()
