import json, os

BASE = "/private/tmp/claude-501/-Users-maximilianguo/85340590-e7fb-4025-b3a4-ad5761ca724d/scratchpad"
DATA = os.path.join(BASE, "jetlag_data")

with open(os.path.join(BASE, "app_shell.html")) as f:
    shell = f.read()

with open(os.path.join(DATA, "geo_data_block.js")) as f:
    geo_block = f.read()

with open(os.path.join(DATA, "vta_line_topology.json")) as f:
    topo = json.load(f)

lines_js = json.dumps([{"name": l["name"], "color": l["color"], "stations_in_order": l["stations_in_order"]} for l in topo["lines"]], separators=(",", ":"))
topo_block = f"const VTA_LINES = {lines_js};"

out = shell.replace("/*GEO_DATA_PLACEHOLDER*/", geo_block)
out = out.replace("/*VTA_TOPOLOGY_PLACEHOLDER*/", topo_block)

assert "GEO_DATA_PLACEHOLDER" not in out
assert "VTA_TOPOLOGY_PLACEHOLDER" not in out

outpath = os.path.join(BASE, "jetlag_map.html")
with open(outpath, "w") as f:
    f.write(out)

print("wrote", outpath, len(out.encode("utf-8")), "bytes")
