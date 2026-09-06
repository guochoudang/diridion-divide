import json, re, os

D = os.path.dirname(__file__)

def load(name):
    with open(os.path.join(D, name)) as f:
        return json.load(f)

def exists(name):
    return os.path.exists(os.path.join(D, name))

def r5(x):
    return round(x, 5)

def norm_name(s):
    return s.replace("’", "'").replace("‘", "'")

def clean_simple(items):
    out = []
    for it in items:
        row = {"n": norm_name(it["name"]), "a": r5(it["lat"]), "o": r5(it["lon"])}
        out.append(row)
    return out

def from_raw_overpass(filename, fallback_label):
    """Convert a raw Overpass response into {name,lat,lon} records, keeping
    unnamed features (labeled generically) instead of silently dropping them —
    an unnamed park is still real territory for nearest-neighbor purposes."""
    raw = load(filename)
    out = []
    unnamed_i = 0
    for el in raw["elements"]:
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("name:en")
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        if not name:
            unnamed_i += 1
            name = f"Unnamed {fallback_label}"
        out.append({"name": name.strip(), "lat": lat, "lon": lon})
    print(f"  {filename}: {len(out)} total, {unnamed_i} unnamed (kept, generically labeled)")
    return out

def downsample(pts, max_pts=5):
    """Keep at most max_pts points (always including first and last) — used
    for unnamed minor waterways, where we need the shape for distance
    purposes but full point-by-point detail isn't worth the size/render cost."""
    if len(pts) <= max_pts:
        return pts
    step = (len(pts) - 1) / (max_pts - 1)
    idxs = sorted(set(round(i * step) for i in range(max_pts)))
    return [pts[i] for i in idxs]

def split_named_unnamed_lines(filename):
    """Convert raw Overpass 'out geom' way elements (rivers/streams) into line
    records. Named ways (the creeks/rivers someone would actually recognize)
    keep their FULL node-by-node geometry and get rendered + labeled. Unnamed
    ways (mostly tiny unlabeled drainage fragments — there are thousands) are
    kept only for nearest-water distance accuracy, with simplified geometry,
    and are never drawn or labeled — rendering ~10k anonymous line fragments
    would be pure clutter with no way for a player to identify them anyway."""
    raw = load(filename)
    named, unnamed = [], []
    for el in raw["elements"]:
        geom = el.get("geometry")
        if not geom or len(geom) < 2:
            continue
        tags = el.get("tags", {})
        name = tags.get("name") or tags.get("name:en")
        pts = [[r5(p["lat"]), r5(p["lon"])] for p in geom]
        if name:
            named.append({"name": name.strip(), "pts": pts})
        else:
            unnamed.append({"pts": downsample(pts)})
    print(f"  {filename}: {len(named)} named ways (full geometry, rendered), {len(unnamed)} unnamed ways (simplified, distance-only)")
    return named, unnamed

vta = load("vta_stations.json")
theatres = load("movie_theatres.json")

malls = from_raw_overpass("shopping_malls_raw_full.json", "shopping mall") if exists("shopping_malls_raw_full.json") else load("shopping_malls.json")
theatres = from_raw_overpass("movie_theatres_raw_full.json", "movie theatre") if exists("movie_theatres_raw_full.json") else load("movie_theatres.json")
hospitals = from_raw_overpass("hospitals_raw_full.json", "hospital") if exists("hospitals_raw_full.json") else load("hospitals.json")
parks = from_raw_overpass("public_parks_raw_full.json", "park")
libraries = from_raw_overpass("libraries_raw_full.json", "library")

# Point-type water (lakes/reservoirs/bay/ponds)
if exists("water_points_raw_full.json"):
    water = from_raw_overpass("water_points_raw_full.json", "body of water")
else:
    water = load("water_bodies.json")  # old dataset (named natural=water only) as fallback

# Filter junk water names (evaporation-pond codes like "A1", "A10;A11;A14")
def is_junk_water_name(name):
    return bool(re.match(r'^[A-Z0-9;\-]+$', name)) and len(name) <= 10

water_clean = [w for w in water if not is_junk_water_name(w["name"])]
print("water points:", len(water), "->", len(water_clean))

def clean_water(items):
    out = []
    for it in items:
        row = {"n": norm_name(it["name"]), "a": r5(it["lat"]), "o": r5(it["lon"])}
        out.append(row)
    return out

# Line-type water (rivers/streams) — named ways get full geometry + render;
# unnamed ways are kept simplified, for distance accuracy only.
named_lines, unnamed_lines = [], []
if exists("rivers_streams_raw_full.json"):
    named_lines, unnamed_lines = split_named_unnamed_lines("rivers_streams_raw_full.json")
else:
    for fn in ("rivers_raw_full.json", "streams_raw_full.json"):
        if exists(fn):
            n, u = split_named_unnamed_lines(fn)
            named_lines += n; unnamed_lines += u

def clean_rivers(items):
    return [{"n": norm_name(it["name"]), "pts": it["pts"]} for it in items]

def clean_minor_water(items):
    return [{"pts": it["pts"]} for it in items]

data = {
    "VTA": clean_simple(vta),
    "MALLS": clean_simple(malls),
    "PARKS": clean_simple(parks),
    "THEATRES": clean_simple(theatres),
    "HOSPITALS": clean_simple(hospitals),
    "LIBRARIES": clean_simple(libraries),
    "WATER": clean_water(water_clean),
}

for k, v in data.items():
    print(k, len(v))

rivers_clean = clean_rivers(named_lines)
minor_water_clean = clean_minor_water(unnamed_lines)
print("RIVERS (named, rendered)", len(rivers_clean))
print("MINOR_WATER (unnamed, distance-only)", len(minor_water_clean))

lines = []
for k, v in data.items():
    lines.append(f"const GEO_{k} = {json.dumps(v, separators=(',', ':'))};")
lines.append(f"const GEO_RIVERS = {json.dumps(rivers_clean, separators=(',', ':'))};")
lines.append(f"const GEO_MINOR_WATER = {json.dumps(minor_water_clean, separators=(',', ':'))};")

block = "\n".join(lines)
with open(os.path.join(D, "geo_data_block.js"), "w") as f:
    f.write(block)

print("block size bytes:", len(block.encode("utf-8")))
