# 21 November 2026 — World News in One Image

Entry for make.fun competition `news-image-20261121`
("Sum up 21 November's world news in one image", $100).

## Run

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 PNG, ~20 KB)
```

`main.py` is Python 3.13, standard library only, no network.
It draws the image pixel by pixel with its own tiny raster canvas
and 5x7 bitmap font, then encodes the PNG itself. There is no
randomness and no clock, so two runs write byte-identical files.

## What the image shows

A newspaper front page dated **Saturday 21 November 2026** with six
main stories and a ticker, all reported on that day:

1. **Iran strikes U.S. bases in Bahrain** — Tehran sought talks to
   end the war; President Trump called its terms unacceptable.
2. **Russian missile hits Kryvyi Rih, Ukraine** — 2 killed, dozens
   wounded in the city centre.
3. **Mexico captures cartel boss "El Chapo Isidro"** — FBI
   most-wanted Fausto Isidro Meza Flores seized in Sinaloa;
   violence after the raid left 11 dead.
4. **COP31 talks run into overtime** — Antalya, Turkey; nations
   split over fossil fuels and finance.
5. **AI sell-off slides U.S. stocks** — chip shares plunge; Nvidia
   faces an SEC accounting probe.
6. **AI "solves greatest math riddle"** — an Anthropic researcher
   claimed a Claude breakthrough (shown as a claim, not as fact).

Ticker: FBI and U.S. Agriculture Department databases breached by
hackers; nations open a path to a "killer robots" pact; BepiColombo
arrives at Mercury; bacteria-carrying mosquitoes cut dengue cases
among children in Brazil.

Stories were cross-checked across the day's reporting (Reuters,
AP via syndication, The Japan Times, The Economic Times, Dawn,
OneTurn News day report for 2026-11-21).

## License

MIT — see `LICENSE`.
