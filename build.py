#!/usr/bin/env python3
"""Generate R2 gallery HTML with presigned URLs (v2 — enhanced picks)."""
import subprocess
import html
import os
import sys
from pathlib import Path

MC = os.path.expanduser("~/.local/bin/mc")
BUCKET = "r2/cdt-heritage-assets"

# slot_id, slot_title, items: [(recommended, kind, label, r2_path)]
SLOTS = [
    ("A", "Home hero — DRONE VIDEO", [
        (True,  "video", "dji-0066.mp4",                          "videos/dji-0066.mp4"),
        (False, "video", "dji-0071.mp4",                          "videos/dji-0071.mp4"),
        (False, "video", "dji-0073.mp4",                          "videos/dji-0073.mp4"),
        (False, "video", "dji-0076.mp4",                          "videos/dji-0076.mp4"),
        (False, "video", "drive-past-03-22.mp4 (ground-level)",   "blair-videos/drive-past-03-22.mp4"),
    ]),
    ("B", "Home hero — STATIC POSTER (also valid as full hero replacement)", [
        (True,  "image", "DJI_0716.JPG (Drone shots / pro)",      "photos/heritage-marketing/Photographs with permission/Drone shots/DJI_0716.JPG"),
        (False, "image", "DJI_0649.JPG (Drone shots / pro)",      "photos/heritage-marketing/Photographs with permission/Drone shots/DJI_0649.JPG"),
        (False, "image", "DJI_0067.JPG (Bob Kerr)",               "photos/heritage-marketing/Photographs with permission/Bob Kerr/DJI_0067.JPG"),
        (False, "image", "DJI_0072.JPG (Bob Kerr)",               "photos/heritage-marketing/Photographs with permission/Bob Kerr/DJI_0072.JPG"),
        (False, "image", "DJI_0075.JPG (Bob Kerr)",               "photos/heritage-marketing/Photographs with permission/Bob Kerr/DJI_0075.JPG"),
        (False, "image", "DJI_0080.JPG (Bob Kerr)",               "photos/heritage-marketing/Photographs with permission/Bob Kerr/DJI_0080.JPG"),
        (False, "image", "Susans First Drone Photo.JPG",          "photos/heritage-marketing/Photographs with permission/Bob Kerr/Susans First Drone Photo.JPG"),
        (False, "image", "drones snow allotments blue.JPG",       "photos/heritage-marketing/Photographs with permission/Bob Kerr/culty snow/drones snow allotments blue.JPG"),
        (False, "image", "drone snow museum solo.JPG",            "photos/heritage-marketing/Photographs with permission/Bob Kerr/culty snow/drone snow museum solo.JPG"),
        (False, "image", "Aerial 1948.png (historical)",          "photos/museum/Aerial 1948.png"),
    ]),
    ("C", "/camp hero", [
        (True,  "image", "Camp Entrance.JPG (Bob Kerr)",          "photos/heritage-marketing/Photographs with permission/Bob Kerr/Camp Entrance.JPG"),
        (False, "image", "aerial-of-self-catering-and-cafe.jpg",  "blair-photos/working-groups/website/aerial-of-self-catering-and-cafe.jpg"),
        (False, "image", "camp entrance 2.JPG (Bob Kerr)",        "photos/heritage-marketing/Photographs with permission/Bob Kerr/camp entrance 2.JPG"),
        (False, "image", "camp-low-sun.jpg (atmospheric)",        "blair-photos/pictures/camp/camp-low-sun.jpg"),
        (False, "image", "DJI_0716.JPG",                          "photos/heritage-marketing/Photographs with permission/Drone shots/DJI_0716.JPG"),
        (False, "image", "Officers Mess.JPG (heritage)",          "photos/heritage-marketing/Photographs with permission/Bob Kerr/Officers Mess.JPG"),
        (False, "image", "sign-at-entrance-9663.jpg",             "blair-photos/pictures/camp/sign-at-entrance-9663.jpg"),
    ]),
    ("D", "/museum hero", [
        (True,  "image", "Aerial 1948.png (historical aerial)",   "photos/museum/Aerial 1948.png"),
        (False, "image", "Museum.JPG (Bob Kerr — modern entrance)", "photos/heritage-marketing/Photographs with permission/Bob Kerr/Museum.JPG"),
        (False, "image", "Museum Entrance.JPG (Bob Kerr)",        "photos/heritage-marketing/Photographs with permission/Bob Kerr/Museum Entrance.JPG"),
        (False, "image", "1948 aerial camp.jpg",                  "photos/museum/1948 aerial camp.jpg"),
        (False, "image", "camp-aerial48.jpg",                     "blair-photos/heritage/museum/wartime/camp-aerial48.jpg"),
        (False, "image", "museum-entrance-sign-8742.jpg",         "blair-photos/heritage/visuals/museum-entrance-sign-8742.jpg"),
        (False, "image", "old map of cultybraggan 1980s",         "photos/museum/old map of cultybraggan 1980s found on site.png"),
    ]),
    ("E", "/about hero", [
        (True,  "image", "Carry On Culty crowd 2023",             "photos/events/2023/Carry On Culty '23 Photos/20230528_113109.jpg"),
        (False, "image", "openday-s004.jpg",                      "blair-photos/heritage/visuals/openday-s004.jpg"),
        (False, "image", "door-open-day-resized.jpg",             "blair-photos/heritage/visuals/door-open-day-resized.jpg"),
        (False, "image", "tours.jpg",                             "blair-photos/heritage/visuals/tours.jpg"),
        (False, "image", "raising-fences-04-23.jpg (community)",  "blair-photos/pictures/camp/raising-fences-04-23.jpg"),
        (False, "image", "Carry On Culty 124134",                 "photos/events/2023/Carry On Culty '23 Photos/20230528_124134.jpg"),
    ]),
    ("F", "/get-involved hero", [
        (True,  "image", "pedal-power-cinema-night.jpg",          "blair-photos/heritage/visuals/pedal-power-cinema-night-in-the-jail-block.jpg"),
        (False, "image", "comrie-cubs.jpg",                       "blair-photos/working-groups/cubs-and-scouts/comrie-cubs.jpg"),
        (False, "image", "cubs-hut-activity.jpg",                 "blair-photos/working-groups/cubs-and-scouts/cubs-hut-activity.jpg"),
        (False, "image", "ccw-wildflower-discovery-2022",         "blair-photos/working-groups/hill-land-wg/ccw-wildflower-discovery-session-25-june-2022.jpg"),
        (False, "image", "Outdoor theatre 2023",                  "photos/events/Event photos/Outdoor theatre/20230824_204513.jpg"),
        (False, "image", "20230805_134854.jpg (event crowd)",     "photos/events/Event photos/20230805_134854.jpg"),
    ]),
    ("G", "/contact hero (small banner above contact cards)", [
        (True,  "image", "Camp Entrance.JPG (Bob Kerr)",          "photos/heritage-marketing/Photographs with permission/Bob Kerr/Camp Entrance.JPG"),
        (False, "image", "sign-at-entrance-9663.jpg",             "blair-photos/pictures/camp/sign-at-entrance-9663.jpg"),
        (False, "image", "aerial-of-self-catering-and-cafe.jpg",  "blair-photos/working-groups/website/aerial-of-self-catering-and-cafe.jpg"),
    ]),
    ("H", "/projects hero", [
        (True,  "image", "DJI_0716.JPG (broad survey shot)",      "photos/heritage-marketing/Photographs with permission/Drone shots/DJI_0716.JPG"),
        (False, "image", "aerial-view-from-north.png",            "blair-photos/working-groups/renewable-energy/aerial-view-from-north.png"),
        (False, "image", "DJI_0067.JPG (Bob Kerr)",               "photos/heritage-marketing/Photographs with permission/Bob Kerr/DJI_0067.JPG"),
    ]),
    ("I", "/projects/orchard hero", [
        (True,  "image", "Orchard 1.JPG (Bob Kerr)",              "photos/heritage-marketing/Photographs with permission/Bob Kerr/Orchard 1.JPG"),
        (False, "image", "Orchard 2.JPG (Bob Kerr)",              "photos/heritage-marketing/Photographs with permission/Bob Kerr/Orchard 2.JPG"),
        (False, "image", "Orchard 3.JPG (Bob Kerr)",              "photos/heritage-marketing/Photographs with permission/Bob Kerr/Orchard 3.JPG"),
        (False, "image", "comrie-community-orchard-1.png",        "blair-photos/working-groups/website/comrie-community-orchard-1.png"),
        (False, "image", "Allotments 1.JPG (Bob Kerr)",           "photos/heritage-marketing/Photographs with permission/Bob Kerr/Allotments 1.JPG"),
        (False, "image", "allotment-cage.jpg",                    "blair-photos/pictures/community-groups/allotments/allotment-cage.jpg"),
    ]),
    ("J", "/projects/woodland hero — major upgrade vs v1", [
        (True,  "image", "woodland-panorama-bluebells.jpg",       "blair-photos/pictures/community-groups/woodland/woodland-panorama-bluebells.jpg"),
        (False, "image", "woodland-sunset.jpg",                   "blair-photos/pictures/community-groups/woodland/woodland-sunset.jpg"),
        (False, "image", "woodland-mother-and-child.jpg",         "blair-photos/working-groups/hill-land-wg/woodland-mother-and-child.jpg"),
        (False, "image", "ccw-wildflower-discovery-2022",         "blair-photos/working-groups/hill-land-wg/ccw-wildflower-discovery-session-25-june-2022.jpg"),
        (False, "image", "wild-flowers-scabiosa.jpg",             "blair-photos/working-groups/paths/cdt-clu/wild-flowers-scabiosa.jpg"),
    ]),
    ("K", "/projects/climate-action hero", [
        (True,  "image", "aerial-view-from-north-with-arrow.png", "blair-photos/working-groups/renewable-energy/aerial-view-from-north-with-arrow.png"),
        (False, "image", "hydro-pipe-line-aerial-view.png",       "blair-photos/working-groups/renewable-energy/hydro-pipe-line-aerial-view.png"),
        (False, "image", "caledonianclimate-peatland-survey",     "blair-photos/working-groups/renewable-energy/caledonianclimate-peatland-survey-cultybraggan.jpg"),
        (False, "image", "aerial-view-from-north (no arrow)",     "blair-photos/working-groups/renewable-energy/aerial-view-from-north.png"),
        (False, "image", "map-of-milntuim-hydro.png",             "blair-photos/working-groups/renewable-energy/map-of-milntuim-hydro.png"),
    ]),
    ("L", "/projects/business-units hero", [
        (True,  "image", "Cafe 21.JPG (Bob Kerr — actual tenant)", "photos/heritage-marketing/Photographs with permission/Bob Kerr/Cafe 21.JPG"),
        (False, "image", "Building 109.JPG",                      "photos/heritage-marketing/Photographs with permission/Bob Kerr/building 109.JPG"),
        (False, "image", "Building 61.JPG",                       "photos/heritage-marketing/Photographs with permission/Bob Kerr/Building 61.JPG"),
        (False, "image", "Hut 25.JPG",                            "photos/heritage-marketing/Photographs with permission/Bob Kerr/Hut 25.JPG"),
        (False, "image", "Hut 7.JPG",                             "photos/heritage-marketing/Photographs with permission/Bob Kerr/hut 7.JPG"),
        (False, "image", "camp-21-cafe.jpg",                      "blair-photos/working-groups/website/camp-21-cafe.jpg"),
        (False, "image", "doorway-and-outside-cafe-21.jpg",       "blair-photos/working-groups/website/doorway-and-outside-cafe-21.jpg"),
    ]),
    ("M", "Accommodation tile examples (per-hut images go in accommodation.images[])", [
        (True,  "image", "Self Catering.JPG (Bob Kerr — exterior)", "photos/heritage-marketing/Photographs with permission/Bob Kerr/Self Catering.JPG"),
        (False, "image", "Hut 25.JPG",                            "photos/heritage-marketing/Photographs with permission/Bob Kerr/Hut 25.JPG"),
        (False, "image", "Hut 7.JPG",                             "photos/heritage-marketing/Photographs with permission/Bob Kerr/hut 7.JPG"),
        (False, "image", "Hut 34 bedroom (interior)",             "photos/self-catering/Hut 34 bedroom.jpg"),
        (False, "image", "Hut 34 bathroom (interior)",            "photos/self-catering/Hut 34 bathroom.jpg"),
        (False, "image", "Facebook (10).png",                     "photos/self-catering/Facebook (10).png"),
        (False, "image", "Facebook (11).png",                     "photos/self-catering/Facebook (11).png"),
        (False, "image", "hut1-restored.jpg",                     "blair-photos/pictures/camp/hut1-restored.jpg"),
    ]),
    ("N", "Museum exhibit candidates", [
        (False, "image", "British+Soldier.jpg",                   "photos/museum/British+Soldier.jpg"),
        (False, "image", "Boy in Polish kitchens camp WW2.jpg",   "photos/museum/Boy in Polish kitchens camp WW2.jpg"),
        (False, "image", "Maimie MacPherson cinema.jpg",          "photos/museum/Maimie MacPherson cinema.jpg"),
        (False, "image", "Jim Thomson and lathe.JPG",             "photos/museum/Jim Thomson and lathe.JPG"),
        (False, "image", "model ship made by POW here.jpg",       "photos/historical-donations/model ship made by POW here.jpg"),
        (False, "image", "Cartoon_Collection_0001.jpg",           "photos/cartoons/Cartoon_Collection_0001.jpg"),
        (False, "image", "Bunte_Buhne_0001.jpg",                  "photos/bunte-buhne/Bunte_Buhne_0001.jpg"),
        (False, "image", "old map of cultybraggan 1980s",         "photos/museum/old map of cultybraggan 1980s found on site.png"),
        (False, "image", "mpnissenhut.jpg (POW letters)",         "blair-photos/heritage/museum/pix5-letters/mpnissenhut.jpg"),
        (False, "image", "insidehut.jpg (POW letters)",           "blair-photos/heritage/museum/pix5-letters/insidehut.jpg"),
        (False, "image", "compoundplan.jpg (POW letters)",        "blair-photos/heritage/museum/pix5-letters/compoundplan.jpg"),
        (False, "image", "1955 postacard of the camp",            "photos/museum/1955 postacard of the camp.jpg"),
    ]),
    ("O", "Bob Kerr area tour — every part of the camp (use anywhere)", [
        (False, "image", "Cafe 21.JPG",                           "photos/heritage-marketing/Photographs with permission/Bob Kerr/Cafe 21.JPG"),
        (False, "image", "Camp Entrance.JPG",                     "photos/heritage-marketing/Photographs with permission/Bob Kerr/Camp Entrance.JPG"),
        (False, "image", "Museum.JPG",                            "photos/heritage-marketing/Photographs with permission/Bob Kerr/Museum.JPG"),
        (False, "image", "Self Catering.JPG",                     "photos/heritage-marketing/Photographs with permission/Bob Kerr/Self Catering.JPG"),
        (False, "image", "Officers Mess.JPG",                     "photos/heritage-marketing/Photographs with permission/Bob Kerr/Officers Mess.JPG"),
        (False, "image", "Officers Avenue.jpg",                   "photos/heritage-marketing/Photographs with permission/Bob Kerr/Officers Avenue.jpg"),
        (False, "image", "Orchard 1.JPG",                         "photos/heritage-marketing/Photographs with permission/Bob Kerr/Orchard 1.JPG"),
        (False, "image", "parade ground.JPG",                     "photos/heritage-marketing/Photographs with permission/Bob Kerr/parade ground.JPG"),
        (False, "image", "Bunker 1.JPG",                          "photos/heritage-marketing/Photographs with permission/Bob Kerr/Bunker 1.JPG"),
        (False, "image", "Rifle Range.JPG",                       "photos/heritage-marketing/Photographs with permission/Bob Kerr/Rifle Range.JPG"),
        (False, "image", "Assault Course 1.JPG",                  "photos/heritage-marketing/Photographs with permission/Bob Kerr/Assault Course 1.JPG"),
        (False, "image", "Cultybraggan Farm.JPG",                 "photos/heritage-marketing/Photographs with permission/Bob Kerr/Cultybraggan Farm.JPG"),
    ]),
    ("P", "Long-form video extras", [
        (False, "video", "heritage-revue.mp4 (5.5 MB — easy embed)", "blair-videos/heritage-revue.mp4"),
        (False, "video", "drive-past-03-22.mp4 (91 MB)",          "blair-videos/drive-past-03-22.mp4"),
        (False, "video", "clodagh-bonham-carter-interview (704 MB)", "videos/clodagh-bonham-carter-edited-interview.mp4"),
    ]),
    ("Q", "Atmospheric / mood photos for inline content blocks", [
        (False, "image", "camp-low-sun.jpg",                      "blair-photos/pictures/camp/camp-low-sun.jpg"),
        (False, "image", "woodland-sunset.jpg",                   "blair-photos/pictures/community-groups/woodland/woodland-sunset.jpg"),
        (False, "image", "woodland-panorama-bluebells.jpg",       "blair-photos/pictures/community-groups/woodland/woodland-panorama-bluebells.jpg"),
        (False, "image", "old-pic-of-camp.jpg (vintage)",         "blair-photos/pictures/camp/old-pic-of-camp.jpg"),
        (False, "image", "training.jpg (heritage)",               "blair-photos/pictures/camp/training.jpg"),
        (False, "image", "wild-flowers-scabiosa.jpg",             "blair-photos/working-groups/paths/cdt-clu/wild-flowers-scabiosa.jpg"),
    ]),
    ("R", "Events page candidates (if /events page added later)", [
        (False, "image", "Classic Cars 2023",                     "photos/events/Event photos/Classic Cars/20230820_112845.jpg"),
        (False, "image", "Carry On Culty 2023",                   "photos/events/2023/Carry On Culty '23 Photos/20230528_113109.jpg"),
        (False, "image", "Outdoor theatre 2023",                  "photos/events/Event photos/Outdoor theatre/20230824_204513.jpg"),
        (False, "image", "Strathearn Marathon 2024",              "photos/events/Events 2024/2024-06-09_StrathearnMarathon/20230911_104256.jpg"),
        (False, "image", "Army Veterans Bikers Rally",            "photos/events/Events 2024/Army Veterans Bikers Rally/20231001_134652.jpg"),
        (False, "image", "Tug of War (reenactor)",                "photos/events/reenactor photos/Tug of War 1.jpg"),
        (False, "image", "vikings poster",                        "photos/events/Events Posters/vikings pic.png"),
    ]),
    ("S", "Branding / banners / logos", [
        (False, "image", "cultybraggancampbanner.jpg",            "blair-photos/pictures/banners/cultybraggancampbanner.jpg"),
        (False, "image", "cultybraggancompositebanner.jpg",       "blair-photos/pictures/banners/cultybraggancompositebanner.jpg"),
        (False, "image", "cdt-logo-1.jpg",                        "blair-photos/pictures/cdt-logo-1.jpg"),
        (False, "image", "cdt-logo-2.jpg",                        "blair-photos/pictures/banners/cdt-logo-2.jpg"),
        (False, "image", "comrie-foundation-logo.jpg",            "blair-photos/pictures/banners/comrie-foundation-logo.jpg"),
    ]),
]

def presign(rel_path: str) -> str | None:
    full = f"{BUCKET}/{rel_path}"
    res = subprocess.run([MC, "share", "download", "--expire", "24h", full],
                         capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  FAIL: {rel_path}: {res.stderr.strip()}", file=sys.stderr)
        return None
    for line in res.stdout.splitlines():
        line = line.strip()
        if line.startswith("Share:"):
            return line.split("Share:", 1)[1].strip()
    return None

def main():
    print("Presigning URLs...", file=sys.stderr)
    rendered_slots = []
    nav_links = []
    for slot_id, slot_title, items in SLOTS:
        nav_links.append(f'<a href="#slot-{slot_id}">{slot_id}</a>')
        cards = []
        for recommended, kind, label, r2_path in items:
            url = presign(r2_path)
            if not url:
                cards.append(f'<div class="card error"><div class="label">{html.escape(label)}</div><div class="path">{html.escape(r2_path)}</div><div class="err">presign failed</div></div>')
                continue
            badge = '<span class="star">★ recommended</span>' if recommended else ''
            if kind == "video":
                media = f'<video controls preload="metadata" src="{html.escape(url)}"></video>'
            else:
                media = f'<a href="{html.escape(url)}" target="_blank" rel="noopener"><img loading="lazy" src="{html.escape(url)}" alt="{html.escape(label)}"></a>'
            cards.append(f'<div class="card{" pick" if recommended else ""}">{media}<div class="meta"><div class="label">{html.escape(label)} {badge}</div><div class="path">{html.escape(r2_path)}</div></div></div>')
            print(f"  ok: {r2_path}", file=sys.stderr)
        rendered_slots.append(f'<section id="slot-{slot_id}"><h2>Slot {slot_id} — {html.escape(slot_title)}</h2><div class="grid">{"".join(cards)}</div></section>')

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CDT website — R2 asset picks (v2)</title>
<style>
  :root {{ --red: #b3343b; --red-soft: #f7e6e8; --bg: #f4f4f3; --line: #e3e3e0; --ink: #222; --muted: #777; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; margin: 0; background: var(--bg); color: var(--ink); }}
  header {{ background: white; border-bottom: 1px solid var(--line); padding: 24px 32px; position: sticky; top: 0; z-index: 10; }}
  header h1 {{ margin: 0 0 6px; font-size: 22px; }}
  header p {{ margin: 0 0 8px; color: var(--muted); font-size: 14px; }}
  nav {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  nav a {{ font-size: 12px; font-weight: 700; padding: 4px 8px; border-radius: 4px; background: var(--red-soft); color: var(--red); text-decoration: none; }}
  nav a:hover {{ background: var(--red); color: white; }}
  main {{ max-width: 1500px; margin: 0 auto; padding: 24px 32px 80px; }}
  section {{ margin-top: 40px; scroll-margin-top: 140px; }}
  section h2 {{ font-size: 16px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--red); border-bottom: 1px solid var(--line); padding-bottom: 8px; margin-bottom: 18px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }}
  .card {{ background: white; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; box-shadow: 0 1px 2px rgba(0,0,0,0.03); display: flex; flex-direction: column; }}
  .card.pick {{ border-color: var(--red); box-shadow: 0 0 0 2px var(--red-soft); }}
  .card img, .card video {{ width: 100%; aspect-ratio: 16/10; object-fit: cover; display: block; background: #000; }}
  .card a {{ display: block; }}
  .card.error {{ padding: 14px; }}
  .meta {{ padding: 10px 12px 14px; }}
  .label {{ font-weight: 600; font-size: 13px; line-height: 1.3; }}
  .path {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 11px; color: var(--muted); margin-top: 4px; word-break: break-all; }}
  .err {{ color: #b00; font-size: 12px; margin-top: 6px; }}
  .star {{ display: inline-block; background: var(--red); color: white; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 6px; border-radius: 4px; margin-left: 4px; vertical-align: middle; }}
</style>
</head>
<body>
<header>
  <h1>CDT website — image &amp; video picks from R2 (v2)</h1>
  <p>Click any image to open full-size in a new tab. Presigned URLs valid 24 hours from generation. ★ = recommended.</p>
  <nav>{"".join(nav_links)}</nav>
</header>
<main>
{"".join(rendered_slots)}
</main>
</body>
</html>"""

    out = Path("/tmp/r2-gallery/index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_doc)
    print(f"\nWrote {out}", file=sys.stderr)
    print(f"Total slots: {len(SLOTS)}; total items: {sum(len(items) for _, _, items in SLOTS)}", file=sys.stderr)

if __name__ == "__main__":
    main()
