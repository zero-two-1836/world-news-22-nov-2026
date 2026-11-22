# World News — Sunday 22 November 2026

One image that sums up the world's news of Sunday 22 November 2026, in the
style of a newspaper front page: a hero story plus nine further stories from
around the world.

## The stories

- **Mexico (top story)** — FBI most-wanted cartel boss "El Chapo Isidro"
  captured in Sinaloa; 11 killed as gunmen burn trucks and block roads.
- **Poland** — Russian missiles land on NATO soil; NATO vows to defend
  "every inch" of allied land.
- **Estonia** — shuts all road crossings with Russia from 1 December after a
  GRU-linked sabotage attack.
- **Climate (COP31)** — talks in Antalya run into overtime; the draft deal
  drops all mention of fossil fuels.
- **Peru** — magnitude 6.9 earthquake shakes the Andes; no damage or
  casualties reported.
- **Brazil** — supercell storm flattens Tupanciretã; three dead, 5,000 homes
  damaged.
- **Nigeria** — boat carrying mourners capsizes in Bayelsa; at least 24 dead.
- **France** — sixth weekend of cost-of-living protests; 82,500 march
  nationwide.
- **Markets** — tech stocks plunge on Wall Street and the sell-off spreads
  across Asia and Europe.
- **United States** — Trump warns US firms building AI data centres abroad
  face a "tremendous tax".

Sources: Reuters, Associated Press, AFP, CNN, USGS.

## How it is made

`build_image.py` draws the infographic with Pillow at 2x supersampling
(2048x2048) and downscales it to 1024x1024, producing `entry.png`
(1024x1024, under 1 MiB). The render is fully deterministic: fixed palette,
fixed fonts, no randomness, no timestamps — every run produces identical
bytes. `main.py` (standard library only) copies `entry.png` to the output
directory given by `MAKEFUN_OUTPUT_DIR` (default `/output`).

## Run it

```sh
python3 build_image.py        # regenerate entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copy it to out/entry.png
```

MIT licensed.
