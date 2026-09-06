# Jet Lag Map Data — San Jose Diridon Station (20 mi radius)

Center: lat=37.3297, lon=-121.9032. Radius: 32,186 m (20 mi).
Source: OpenStreetMap via Overpass API (https://overpass-api.de/api/interpreter), fetched 2026-09-04.
All files are JSON arrays of `{name, lat, lon, type}` objects, sorted alphabetically by name.

## Entry counts

| File | Count | Notes |
|---|---|---|
| vta_stations.json | 59 | Deduplicated from 117 raw `railway=stop` nodes (two platform nodes per station, one per direction) by averaging lat/lon per station name. |
| shopping_malls.json | 17 | Includes 3 "Unnamed shopping mall" entries (mall polygons with no `name` tag). |
| public_parks.json | 726 | Filtered to named parks only; 276 unnamed park features were excluded (out of 1,002 raw elements). |
| movie_theatres.json | 24 | All named. |
| hospitals.json | 22 | Named `amenity=hospital` features only; clinics/urgent care excluded. |
| libraries.json | 122 | Includes public library branches plus university/institutional libraries (e.g. several Stanford departmental libraries, which fall within 20 mi of Diridon). 2 unnamed library nodes excluded. |
| water_bodies.json | 549 | Breakdown: 367 named streams, 162 lakes/reservoirs (`natural=water` + name), 18 rivers, 2 bay segments (San Francisco Bay). |

## Caveats / data quality notes

- **VTA stations**: Tagging scheme used was `railway=stop` + `light_rail=yes` + `network~"VTA"`. BART stations were excluded by construction. Note VTA has its own station literally named "Berryessa" (Orange Line), distinct from the nearby BART "Berryessa/North San José" station — both are legitimate, separate stations; only the VTA one is in this file.
- **Streams/rivers are linear features**: `out center;` returns a rough centroid of each way, not the nearest point on the line. Every `river`/`stream` entry has `"linear": true` and a `segment_count` field showing how many raw OSM way segments were averaged into that centroid — for long streams this can be a poor stand-in for "closest point," so straight-line distance to these entries is a simplification.
- **Shopping malls**: "Westfield Valley Fair" and "Valley Fair Westfield" both appear as separate OSM-tagged features (likely one node for the complex, one for a building/anchor) — not merged since the name strings differ; treat as the same real-world location if used in-game. "Vallco Mall" is included as tagged in OSM even though the physical mall has been largely redeveloped/demolished in recent years.
- **Libraries**: 122 is higher than a "public library" search alone would suggest because it also picks up Stanford's departmental/special libraries and a few private/institutional libraries. No filtering was applied beyond requiring `amenity=library` + a name, per the original query spec.
- **Public parks**: 726 is large but per-spec (instructions said to expect hundreds and keep all named ones). No further curation (e.g. removing small pocket parks) was applied.
- **Overpass reliability**: The API returned transient "server too busy" / timeout errors a few times during this run (during query experimentation, not on final runs). All 7 final category queries succeeded (with a 15s retry backoff where needed); no category needs a re-run. Coordinates are OSM node/way/relation centers rounded to 6 decimal places (~0.11 m precision).
