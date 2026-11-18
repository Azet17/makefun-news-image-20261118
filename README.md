# The World Today — Wednesday 18 November 2026

[![make.fun](https://make.fun/bounty/news-image-20261118)](https://make.fun/bounty/news-image-20261118)
[![make.fun bounty: news-image-20261118](https://make.fun/bounty/news-image-20261118)](https://make.fun/bounty/news-image-20261118)

Entry for the [make.fun news-image-20261118 bounty](https://make.fun/bounty/news-image-20261118):
one image that sums up the world news of Wednesday 18 November 2026.

## What it is

A newspaper front page — masthead **THE WORLD TODAY**, the date
**WEDNESDAY 18 NOVEMBER 2026**, and six stories, each with a short headline,
a one-line summary, and a pictogram drawn from geometric shapes only
(no photos, no AI images, no copied artwork).

## The six stories (all first reported 18 November 2026)

1. **Trump in Manila for Quad talks** — the US president opens his Asia trip
   with Quad allies, ahead of a visit to China. (AP / Reuters)
2. **Ukraine hits Crimea bridge again** — Kyiv strikes the bridge for a second
   day as Russia pounds bridges in Kyiv. (DW)
3. **Cyclone Akvan strengthens** — storm over the Bay of Bengal set to turn
   severe; flights cancelled. (IMD via Indian press)
4. **Israel elects new speaker** — the Knesset picks Matan Kahana, an ally of
   Eisenkot, in a blow to Netanyahu. (New York Times)
5. **Nvidia beats forecasts** — the chip giant tops expectations and its
   shares climb. (BBC)
6. **Dhoni ends IPL career** — MS Dhoni retires from playing; Chennai Super
   Kings name him team mentor. (The Times of India / Indian Express)

## How it works

- `draw.py` renders `entry.png` (1024×1024) with Pillow. It is the only file
  that needs Pillow, and it runs on the build machine, not in the grader.
- `main.py` is the entrypoint: standard library only. It copies the
  pre-rendered `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
  `/output`) and verifies the copy with sha256. It runs with no network.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the image from scratch (needs Pillow):

```sh
python3 draw.py
```
