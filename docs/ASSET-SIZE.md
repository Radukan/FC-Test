# Asset size

Second Nature ships one large archive, and almost all of it is sprite data. This
records what was measured, what was changed, and what was deliberately not.

## Where the bytes were

Audit of the 0.10.0 release archive (114.0 MB, 711 entries):

| Class | ZIP MB | Share |
|---|---:|---:|
| PNG (630 files) | 107.2 | **94.0%** |
| OGG (9 files) | 6.5 | 5.7% |
| Lua / cfg / md / json | 0.3 | 0.3% |

PNGs are already DEFLATE-compressed internally, so the ZIP barely compresses
them further (ratio 0.932). **Archive size is PNG size**; tuning zip settings
achieves nothing.

By subject: character 36.5 MB (32%), machines 32.5 MB, power and trains 21.8 MB,
turrets 11.6 MB.

## What actually drives PNG size

Every candidate was measured on this mod's own atlases rather than assumed. Two
results overturned the obvious plan:

| Technique | Measured result | Used |
|---|---|---|
| Re-saving through PIL | **-4.2%** (files grow) | no |
| `oxipng -o4 --strip safe` | 12.9% | yes, as a second pass |
| **Cropping transparent padding** | **0.3-1.4%** | **no** |
| **Non-integer (1.5x) downscale** | **-210% (files triple)** | **no** |
| Integer 2x downscale | 37-59% | character only |
| **RGB quantisation, alpha preserved** | **20-70%** | **yes, primary** |
| Full palette indexing (alpha in palette) | 81-87% | no |

**Cropping padding is worthless.** Character sheets are only 9-17% non-transparent,
which suggests a large win, but fully transparent regions already collapse to
almost nothing under DEFLATE. Tight-cropping the machine atlases returned 0.3%.

**Non-integer downscaling is actively harmful.** Resampling a 7k-colour sheet by
1.5x produced 40k colours of interpolation noise and made the file three times
larger. Only power-of-two factors are safe.

**The real cost is colour variety.** The renderer emits smooth 24-bit gradients
that PNG's row predictors cannot model, so each pixel costs real bytes. Reducing
the number of distinct colours - at unchanged resolution - is what pays.

**Full palette indexing was rejected despite being the biggest win.** It collapsed
the sprites' 74 alpha levels to 6 and visibly hardened every antialiased edge.

## What was done

`tools/optimize_sprites.py` applies two guarded passes to every shipped PNG:

1. **Quantise RGB only**, copying the alpha channel back verbatim. Soft edges and
   cast shadows stay bit-exact. Budgets are 128 colours for entity atlases and
   192 for icons, technology cards and medallions.
2. **Lossless `oxipng`** filter and deflate search over the result.

Both are guarded three ways: a file is rewritten only when the candidate is
genuinely smaller, the alpha channel is byte-identical, and the result is still
true RGBA. That last check matters - `oxipng` will silently rewrite any
<=256-colour sheet as an indexed image, which the engine's atlas builder and
several tests reject.

`python tools/optimize_sprites.py --check` re-runs the search and fails if any
shipped sprite could still be made smaller, so unoptimised art cannot be
committed.

Measured quality on the pre-existing art: **alpha identical**, PSNR 38-40 dB on
visible pixels, mean error under 1.2/255, resolution unchanged. Above ~40 dB the
difference is not perceptible; the sub-40 cases are dense-gradient sheets where
the error is still around one unit per channel.

The character contributes again separately: the warden is authored from a
ten-tone flat palette specifically so this pass has little left to remove. See
[WARDEN.md](WARDEN.md).

## What was deliberately left alone

* **Audio.** 6.5 MB total, already encoded at 60-110 kbps stereo and 58-61 kbps
  mono. Re-encoding would save 1-2 MB at most and risks the working soundscape.
* **Resolution of machines, turrets, trains and power plants.** These store
  90-107 pixels per tile against vanilla's 65-71. They are already close to
  stock density; halving them would put the mod visibly below the base game.
* **Frame counts and turret directions.** 16-20 frames and 64 directions match
  vanilla convention. Reducing them would produce visible judder.
