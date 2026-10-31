"""Static validation of the whole mod: JSON syntax, cross references, structure templates
(block ids + properties checked against the vanilla 1.20.1 block table) and Java<->content
consistency.  This is NOT a substitute for running the game - it catches broken references.

Usage: python3 validate.py        (exit code 1 when any error is found)
"""
import glob
import gzip
import json
import os
import re
import struct
import sys

from content import BLOCKS, ITEMS, LANG_EXTRA, RECIPES

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, ".."))
RES = os.path.join(PROJ, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", "donbass")
DATA = os.path.join(RES, "data", "donbass")
JAVA = os.path.join(PROJ, "src", "main", "java")
REF = os.path.join(HERE, "reference")

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:  # noqa: BLE001
        err(f"invalid JSON {os.path.relpath(path, PROJ)}: {e}")
        return None


def refj(name):
    with open(os.path.join(REF, name), encoding="utf-8") as f:
        return json.load(f)


VBLOCKS = refj("vanilla_blocks_1.20.1.json")      # only blocks that HAVE properties: id -> [props, default]
for _bid in refj("vanilla_block_ids_1.20.1.json"):  # full registry: property-less blocks (dirt, air, ...)
    VBLOCKS.setdefault(_bid, [{}, {}])
VITEMS = set(refj("vanilla_items_1.20.1.json"))
VWG = refj("vanilla_worldgen_names_1.20.1.json")

# ---- property tables for our own blocks, derived from the block kind ----------
BOOL = ["true", "false"]
FACING4 = ["north", "south", "west", "east"]
KIND_PROPS = {
    "cube": {}, "falling": {}, "magma": {}, "glass": {},
    "pillar": {"axis": ["x", "y", "z"]},
    "slab": {"type": ["top", "bottom", "double"], "waterlogged": BOOL},
    "stairs": {"facing": FACING4, "half": ["top", "bottom"],
               "shape": ["straight", "inner_left", "inner_right", "outer_left", "outer_right"], "waterlogged": BOOL},
    "pane": {"north": BOOL, "south": BOOL, "east": BOOL, "west": BOOL, "waterlogged": BOOL},
}
OWN_BLOCKS = {b["id"]: KIND_PROPS[b["kind"]] for b in BLOCKS}
OWN_ITEM_IDS = {i["id"] for i in ITEMS} | set(OWN_BLOCKS)
VANILLA_BLOCK_IDS = set(VBLOCKS)


def item_exists(ref_id):
    ns, _, name = ref_id.rpartition(":") if ":" in ref_id else ("minecraft", "", ref_id)
    ns = ns or "minecraft"
    return name in OWN_ITEM_IDS if ns == "donbass" else name in VITEMS


# ---- minimal NBT reader -------------------------------------------------------
def read_nbt(buf, off, tid):
    if tid == 1:
        return struct.unpack_from(">b", buf, off)[0], off + 1
    if tid == 2:
        return struct.unpack_from(">h", buf, off)[0], off + 2
    if tid == 3:
        return struct.unpack_from(">i", buf, off)[0], off + 4
    if tid == 4:
        return struct.unpack_from(">q", buf, off)[0], off + 8
    if tid == 5:
        return struct.unpack_from(">f", buf, off)[0], off + 4
    if tid == 6:
        return struct.unpack_from(">d", buf, off)[0], off + 8
    if tid == 8:
        n = struct.unpack_from(">H", buf, off)[0]
        return buf[off + 2:off + 2 + n].decode("utf-8"), off + 2 + n
    if tid == 9:
        et, n = struct.unpack_from(">bi", buf, off)
        off += 5
        out = []
        for _ in range(n):
            v, off = read_nbt(buf, off, et)
            out.append(v)
        return out, off
    if tid == 10:
        d = {}
        while True:
            et = buf[off]
            off += 1
            if et == 0:
                return d, off
            n = struct.unpack_from(">H", buf, off)[0]
            key = buf[off + 2:off + 2 + n].decode("utf-8")
            off += 2 + n
            d[key], off = read_nbt(buf, off, et)
    raise ValueError(f"unsupported NBT tag {tid}")


def read_template(path):
    raw = gzip.open(path).read()
    assert raw[0] == 10, "root is not a compound"
    n = struct.unpack_from(">H", raw, 1)[0]
    root, _ = read_nbt(raw, 3 + n, 10)
    return root


# ---- checks -------------------------------------------------------------------
def check_templates():
    pools = {os.path.relpath(p, os.path.join(DATA, "worldgen", "template_pool"))[:-5].replace(os.sep, "/")
             for p in glob.glob(os.path.join(DATA, "worldgen", "template_pool", "**", "*.json"), recursive=True)}
    loot = {os.path.relpath(p, os.path.join(DATA, "loot_tables"))[:-5].replace(os.sep, "/")
            for p in glob.glob(os.path.join(DATA, "loot_tables", "**", "*.json"), recursive=True)}
    count = blocks_checked = 0
    for path in sorted(glob.glob(os.path.join(DATA, "structures", "**", "*.nbt"), recursive=True)):
        rel = os.path.relpath(path, os.path.join(DATA, "structures"))
        count += 1
        try:
            t = read_template(path)
        except Exception as e:  # noqa: BLE001
            err(f"{rel}: unreadable NBT ({e})")
            continue
        sx, sy, sz = t["size"]
        if t.get("DataVersion") != 3465:
            err(f"{rel}: DataVersion {t.get('DataVersion')} != 3465 (1.20.1)")
        palette = t["palette"]
        for i, entry in enumerate(palette):
            name = entry["Name"]
            ns, _, bid = name.partition(":")
            props = entry.get("Properties", {})
            allowed = OWN_BLOCKS.get(bid) if ns == "donbass" else (VBLOCKS[bid][0] if bid in VBLOCKS else None)
            if allowed is None:
                err(f"{rel}: unknown block {name}")
                continue
            for k, v in props.items():
                if k not in allowed:
                    err(f"{rel}: {name} has no property '{k}'")
                else:
                    ok = allowed[k] if isinstance(allowed[k], list) else [allowed[k]]
                    if v not in [str(x) for x in ok]:
                        err(f"{rel}: {name}[{k}={v}] not in {ok}")
        for b in t["blocks"]:
            blocks_checked += 1
            x, y, z = b["pos"]
            if not (0 <= x < sx and 0 <= y < sy and 0 <= z < sz):
                err(f"{rel}: block at {b['pos']} outside size {t['size']}")
            if b["state"] >= len(palette):
                err(f"{rel}: state index {b['state']} out of palette")
            nbt = b.get("nbt")
            if not nbt:
                continue
            if "LootTable" in nbt:
                lt = nbt["LootTable"].replace("donbass:", "")
                if lt not in loot:
                    err(f"{rel}: loot table {nbt['LootTable']} does not exist")
            if nbt.get("id") == "minecraft:jigsaw":
                p = nbt["pool"]
                if p != "minecraft:empty" and p.replace("donbass:", "") not in pools:
                    err(f"{rel}: jigsaw pool {p} does not exist")
                if nbt["name"] != nbt["target"]:
                    warnings.append(f"{rel}: jigsaw name != target ({nbt['name']} / {nbt['target']})")
    print(f"  templates: {count} files, {blocks_checked} blocks checked")


def check_assets():
    n_models = 0
    for b in BLOCKS:
        i = b["id"]
        if not os.path.isfile(os.path.join(ASSETS, "blockstates", i + ".json")):
            err(f"missing blockstate {i}")
        if not os.path.isfile(os.path.join(ASSETS, "models", "item", i + ".json")):
            err(f"missing item model for block {i}")
        if not os.path.isfile(os.path.join(DATA, "loot_tables", "blocks", i + ".json")):
            err(f"missing loot table {i}")
    for it in ITEMS:
        if not os.path.isfile(os.path.join(ASSETS, "models", "item", it["id"] + ".json")):
            err(f"missing item model {it['id']}")
        if not os.path.isfile(os.path.join(ASSETS, "textures", "item", it["id"] + ".png")):
            err(f"missing item texture {it['id']}")

    def model_exists(ref_id):
        ns, _, p = ref_id.partition(":")
        if ns == "minecraft":
            return True  # vanilla parents (cube_all, slab, stairs, ...) are not validated here
        return os.path.isfile(os.path.join(ASSETS, "models", p + ".json"))

    for p in glob.glob(os.path.join(ASSETS, "blockstates", "*.json")):
        d = load(p)
        if d is None:
            continue
        entries = list((d.get("variants") or {}).values())
        for part in d.get("multipart", []):
            entries.append(part["apply"])
        for e in entries:
            for m in ([e] if isinstance(e, dict) else e):
                if not model_exists(m["model"]):
                    err(f"{os.path.basename(p)}: model {m['model']} missing")
    for p in glob.glob(os.path.join(ASSETS, "models", "**", "*.json"), recursive=True):
        n_models += 1
        d = load(p)
        if d is None:
            continue
        if "parent" in d and not model_exists(d["parent"]):
            err(f"{os.path.relpath(p, ASSETS)}: parent {d['parent']} missing")
        for key, tex in d.get("textures", {}).items():
            if tex.startswith("donbass:"):
                if not os.path.isfile(os.path.join(ASSETS, "textures", tex[8:] + ".png")):
                    err(f"{os.path.relpath(p, ASSETS)}: texture {tex} missing")
    # every texture file should be used (catch typos / dead files)
    used = set()
    for p in glob.glob(os.path.join(ASSETS, "models", "**", "*.json"), recursive=True):
        for tex in (load(p) or {}).get("textures", {}).values():
            if tex.startswith("donbass:"):
                used.add(tex[8:])
    for p in glob.glob(os.path.join(ASSETS, "textures", "**", "*.png"), recursive=True):
        rel = os.path.relpath(p, os.path.join(ASSETS, "textures"))[:-4].replace(os.sep, "/")
        if rel not in used:
            warnings.append(f"texture {rel} is not referenced by any model")
    print(f"  assets: {len(BLOCKS)} blocks, {len(ITEMS)} items, {n_models} models")


def check_lang():
    expected = ({f"block.donbass.{b['id']}" for b in BLOCKS} | {f"item.donbass.{i['id']}" for i in ITEMS}
                | set(LANG_EXTRA))
    for code in ("en_us", "ru_ru", "pl_pl"):
        d = load(os.path.join(ASSETS, "lang", code + ".json"))
        if d is None:
            continue
        if set(d) != expected:
            err(f"lang {code}: missing {sorted(expected - set(d))[:5]} extra {sorted(set(d) - expected)[:5]}")
        for k, v in d.items():
            if not v.strip():
                err(f"lang {code}: empty value for {k}")
    ru = load(os.path.join(ASSETS, "lang", "ru_ru.json")) or {}
    en = load(os.path.join(ASSETS, "lang", "en_us.json")) or {}
    same = [k for k in ru if ru[k] == en.get(k) and k.startswith(("block.", "item."))]
    if same:
        warnings.append(f"lang ru_ru identical to en_us for {len(same)} entries, e.g. {same[:3]}")
    print("  lang: en_us, ru_ru, pl_pl")


def check_recipes_and_loot():
    n = 0
    for p in glob.glob(os.path.join(DATA, "recipes", "*.json")):
        d = load(p)
        if d is None:
            continue
        n += 1
        result = d["result"]["item"] if isinstance(d["result"], dict) else d["result"]
        refs = [result]
        for ing in d.get("ingredients", []):
            refs.append(ing["item"])
        for ing in d.get("key", {}).values():
            refs.append(ing["item"])
        if "ingredient" in d:
            refs.append(d["ingredient"]["item"])
        for r in refs:
            if not item_exists(r):
                err(f"recipe {os.path.basename(p)}: unknown item {r}")
        if d["type"] == "minecraft:crafting_shaped":
            used = set("".join(d["pattern"])) - {" "}
            if used != set(d["key"]):
                err(f"recipe {os.path.basename(p)}: pattern keys {sorted(used)} != key {sorted(d['key'])}")
    for p in glob.glob(os.path.join(DATA, "loot_tables", "**", "*.json"), recursive=True):
        txt = open(p, encoding="utf-8").read()
        d = load(p)
        if d is None:
            continue
        for m in re.finditer(r'"name":\s*"([a-z_]+:[a-z_/]+)"', txt):
            if not item_exists(m.group(1)):
                err(f"loot {os.path.relpath(p, DATA)}: unknown item {m.group(1)}")
    print(f"  recipes: {n}")


def jid(path, base):
    return os.path.relpath(path, base)[:-5].replace(os.sep, "/")


def check_worldgen():
    wg = os.path.join(DATA, "worldgen")
    have = {}
    for sub in ("biome", "configured_carver", "configured_feature", "placed_feature", "noise_settings",
                "density_function", "processor_list", "structure", "structure_set", "template_pool"):
        have[sub] = {jid(p, os.path.join(wg, sub)) for p in
                     glob.glob(os.path.join(wg, sub, "**", "*.json"), recursive=True)}
    for p in glob.glob(os.path.join(DATA, "**", "*.json"), recursive=True):
        load(p)  # syntax of everything

    def has(kind, ref_id, vanilla_key=None):
        ns, _, name = ref_id.partition(":")
        if ns == "donbass":
            return name in have[kind]
        return vanilla_key is None or name in VWG.get(vanilla_key, [])

    for b in ("steppe", "balka"):
        d = load(os.path.join(wg, "biome", b + ".json")) or {"features": [], "carvers": {}}
        if len(d["features"]) != 11:
            err(f"biome {b}: {len(d['features'])} feature steps (need 11)")
        for step in d["features"]:
            for f in step:
                if not has("placed_feature", f, "placed_feature"):
                    err(f"biome {b}: unknown placed feature {f}")
        for c in d["carvers"].get("air", []):
            if not has("configured_carver", c, "configured_carver"):
                err(f"biome {b}: unknown carver {c}")
    for name in have["placed_feature"]:
        d = load(os.path.join(wg, "placed_feature", name + ".json"))
        if d and not has("configured_feature", d["feature"]):
            err(f"placed_feature {name}: unknown configured feature {d['feature']}")
    java_features = set(re.findall(r'FEATURES\.register\("([a-z_]+)"', open(
        os.path.join(JAVA, "com/donbass/mod/registry/ModFeatures.java"), encoding="utf-8").read()))
    for name in have["configured_feature"]:
        d = load(os.path.join(wg, "configured_feature", name + ".json"))
        if d and d["type"].startswith("donbass:") and d["type"][8:] not in java_features:
            err(f"configured_feature {name}: type {d['type']} is not registered in Java ({java_features})")
        if d and d["type"] == "minecraft:ore":
            for tgt in d["config"]["targets"]:
                bid = tgt["state"]["Name"]
                ns, _, n = bid.partition(":")
                if (ns == "donbass" and n not in OWN_BLOCKS) or (ns == "minecraft" and n not in VBLOCKS):
                    err(f"configured_feature {name}: unknown block {bid}")
    for name in have["structure"]:
        d = load(os.path.join(wg, "structure", name + ".json"))
        if d and not has("template_pool", d["start_pool"]):
            err(f"structure {name}: unknown start pool {d['start_pool']}")
    structures_in_sets = set()
    for name in have["structure_set"]:
        d = load(os.path.join(wg, "structure_set", name + ".json"))
        if not d:
            continue
        pl = d["placement"]
        if pl["separation"] >= pl["spacing"]:
            err(f"structure_set {name}: separation must be < spacing")
        if "exclusion_zone" in pl and not has("structure_set", pl["exclusion_zone"]["other_set"]):
            err(f"structure_set {name}: unknown exclusion set")
        for s in d["structures"]:
            structures_in_sets.add(s["structure"][8:])
            if not has("structure", s["structure"]):
                err(f"structure_set {name}: unknown structure {s['structure']}")
    for name in have["structure"] - structures_in_sets:
        err(f"structure {name} is not part of any structure_set (it would never generate)")
    templates = {jid(p, os.path.join(DATA, "structures")) for p in
                 glob.glob(os.path.join(DATA, "structures", "**", "*.nbt"), recursive=True) if True} if False else {
        os.path.relpath(p, os.path.join(DATA, "structures"))[:-4].replace(os.sep, "/")
        for p in glob.glob(os.path.join(DATA, "structures", "**", "*.nbt"), recursive=True)}
    used_templates = set()
    for name in have["template_pool"]:
        d = load(os.path.join(wg, "template_pool", name + ".json"))
        if not d:
            continue
        if d["fallback"] != "minecraft:empty" and not has("template_pool", d["fallback"]):
            err(f"pool {name}: unknown fallback {d['fallback']}")
        for e in d["elements"]:
            el = e["element"]
            loc = el["location"]
            used_templates.add(loc[8:])
            if loc[8:] not in templates:
                err(f"pool {name}: template {loc} missing")
            proc = el["processors"]
            if isinstance(proc, str) and not has("processor_list", proc, "processor_list"):
                err(f"pool {name}: unknown processor list {proc}")
    for t in templates - used_templates:
        warnings.append(f"template {t} is not used by any pool")
    for name in have["processor_list"]:
        d = load(os.path.join(wg, "processor_list", name + ".json"))
        for proc in (d or {}).get("processors", []):
            for r in proc.get("rules", []):
                for ref_id in (r["input_predicate"]["block"], r["output_state"]["Name"]):
                    ns, _, n = ref_id.partition(":")
                    if (ns == "donbass" and n not in OWN_BLOCKS) or (ns == "minecraft" and n not in VBLOCKS):
                        err(f"processor {name}: unknown block {ref_id}")
    ns_ = load(os.path.join(wg, "noise_settings", "steppe.json"))
    dens = load(os.path.join(wg, "density_function", "steppe", "base.json"))
    if ns_ is not None and not has("density_function", ns_["noise_router"]["final_density"]["argument"]):
        err("noise_settings steppe: unknown density function")
    for m in re.finditer(r'"noise":\s*"minecraft:([a-z_]+)"', json.dumps(dens) + json.dumps(ns_)):
        if m.group(1) not in VWG["noise"]:
            err(f"unknown vanilla noise minecraft:{m.group(1)}")
    dim = load(os.path.join(DATA, "dimension", "donbass.json"))
    if dim:
        if not has("noise_settings", dim["generator"]["settings"]):
            err("dimension: unknown noise settings")
        for e in dim["generator"]["biome_source"]["biomes"]:
            if not has("biome", e["biome"]):
                err(f"dimension: unknown biome {e['biome']}")
    for tag in glob.glob(os.path.join(DATA, "tags", "worldgen", "biome", "*.json")):
        for v in (load(tag) or {}).get("values", []):
            if not has("biome", v):
                err(f"tag {os.path.basename(tag)}: unknown biome {v}")
    print(f"  worldgen: {sum(len(v) for v in have.values())} JSON files, {len(templates)} templates")


def check_java():
    reg = open(os.path.join(JAVA, "com/donbass/mod/registry/ModBlocks.java"), encoding="utf-8").read()
    defined_blocks = set(re.findall(r"RegistryObject<Block> ([A-Z_]+) =", reg))
    items_src = open(os.path.join(JAVA, "com/donbass/mod/registry/ModItems.java"), encoding="utf-8").read()
    defined_items = set(re.findall(r"RegistryObject<Item> ([A-Z_]+) =", items_src))
    if defined_blocks != {b["id"].upper() for b in BLOCKS}:
        err("ModBlocks.java is out of date - rerun gen_resources.py")
    if defined_items != {i["id"].upper() for i in ITEMS}:
        err("ModItems.java is out of date - rerun gen_resources.py")
    for p in glob.glob(os.path.join(JAVA, "**", "*.java"), recursive=True):
        src = open(p, encoding="utf-8").read()
        for m in re.finditer(r"ModBlocks\.([A-Z_]+)\b", src):
            if m.group(1) not in defined_blocks and m.group(1) not in ("BLOCKS",):
                err(f"{os.path.basename(p)}: ModBlocks.{m.group(1)} does not exist")
        for m in re.finditer(r"ModItems\.([A-Z_]+)\b", src):
            if m.group(1) not in defined_items and m.group(1) not in ("ITEMS",):
                err(f"{os.path.basename(p)}: ModItems.{m.group(1)} does not exist")
    mods_toml = open(os.path.join(RES, "META-INF", "mods.toml"), encoding="utf-8").read()
    if 'modId="${mod_id}"' not in mods_toml:
        err("mods.toml: modId placeholder missing")
    print(f"  java: {len(defined_blocks)} block + {len(defined_items)} item registrations match content.py")


JAVA_LANG = {"String", "Math", "Override", "Object", "Integer", "Double", "Float", "Long", "Boolean", "Byte",
             "Short", "Character", "Number", "Class", "Exception", "RuntimeException", "IllegalArgumentException",
             "IllegalStateException", "Iterable", "Runnable", "Deprecated", "SuppressWarnings", "FunctionalInterface",
             "Void", "System", "Thread", "Enum", "Record", "SafeVarargs", "CharSequence", "Comparable", "Error"}


def check_java_imports():
    """Heuristic stand-in for the compiler's 'cannot find symbol' on types: every CamelCase type name
    used in a file must be imported, declared in the file, in the same package, or in java.lang."""
    files = glob.glob(os.path.join(JAVA, "**", "*.java"), recursive=True)
    by_pkg = {}
    for p in files:
        by_pkg.setdefault(os.path.dirname(p), set()).add(os.path.basename(p)[:-5])
    for p in files:
        src = open(p, encoding="utf-8").read()
        body = re.sub(r"//[^\n]*|/\*.*?\*/", " ", src, flags=re.S)
        body = re.sub(r'"(?:\\.|[^"\\])*"', '""', body)
        imported = set(re.findall(r"^import\s+(?:static\s+)?[\w.]*\.(\w+);", body, flags=re.M))
        declared = set(re.findall(r"\b(?:class|interface|enum|record)\s+(\w+)", body))
        body_wo_imports = re.sub(r"^(?:import|package)\s[^;]*;", "", body, flags=re.M)
        used = {m.group(1) for m in re.finditer(r"(?<![\w.])([A-Z][a-z][A-Za-z0-9]*)\b", body_wo_imports)}
        generic = {m for m in used if len(m) == 1}
        for name in sorted(used - imported - declared - by_pkg[os.path.dirname(p)] - JAVA_LANG - generic):
            err(f"{os.path.relpath(p, JAVA)}: type '{name}' is not imported/declared (compile error)")
        for name in sorted(imported):                       # unused imports are only a warning
            if not re.search(r"\b" + name + r"\b", body_wo_imports):
                warnings.append(f"{os.path.relpath(p, JAVA)}: unused import {name}")
        pkg = re.search(r"^package\s+([\w.]+);", body, flags=re.M).group(1)
        expected = os.path.relpath(os.path.dirname(p), JAVA).replace(os.sep, ".")
        if pkg != expected:
            err(f"{os.path.relpath(p, JAVA)}: package {pkg} does not match directory {expected}")
    print(f"  java imports: {len(files)} files checked")


def main():
    print("Validating Donbass mod...")
    for fn in (check_templates, check_assets, check_lang, check_recipes_and_loot, check_worldgen, check_java,
               check_java_imports):
        fn()
    for w in warnings:
        print("  warning:", w)
    for e in errors:
        print("  ERROR:", e)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
