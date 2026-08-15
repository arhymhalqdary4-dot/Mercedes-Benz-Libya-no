# Decakila Libya — UI mockup

One self-contained file: `decakila/index.html`. No build step, no dependencies.
Open it directly in a browser, or serve the folder with any static host.

The only network request is the Google Fonts stylesheet (Poppins for English,
Cairo/Tajawal for Arabic). Offline, it falls back to the system sans-serif and
everything else still works.

## Brand

| Token | Value | Where it's used |
| --- | --- | --- |
| `--brand-red` | `#E30613` | Buttons, hero, branches band, accents |
| `--brand-red-dark` / `--brand-red-deep` | `#B4040F` / `#8C030B` | Gradients, hover states |
| `--brand-red-tint` | `#FDECEE` | Icon wells, focus rings |
| Neutrals | `--grey-50` … `--grey-900` | Surfaces, text, borders |

`--brand-red` is the one value to change if you have the exact hex from the
official brand sheet — every red on the page derives from it. It's defined at
the very top of the `:root` block.

### The swoosh

The S-curve from the bottom of the logo is reused as a structural element in
four places: the base of the hero, the top of the branches band, the bottom of
each product image well, and the base of the About panel. The full-width version
is one SVG path, duplicated in two `.swoosh` blocks:

```
M0,110 L1440,110 L1440,24 C1180,102 1010,6 660,62 C430,99 190,104 0,58 Z
```

It mirrors itself in RTL (`html[dir="rtl"] .swoosh svg { transform: scaleX(-1) }`)
so the curve always sweeps with the reading direction.

## Bilingual

The `EN / ع` switch in the header flips `lang`, `dir`, the font stack, the page
title and every tagged string. The choice is stored in `localStorage`; on a first
visit it follows the browser language.

All copy lives in the `T` object at the top of the `<script>` — `T.en` and `T.ar`
share one key set. To add a string:

```html
<p data-i18n="myKey">English default</p>
<input data-i18n-ph="myKeyPh" placeholder="English default">
```

…then add `myKey` to **both** `T.en` and `T.ar`. Nothing else is wired to
language, because layout uses CSS logical properties (`margin-inline`,
`inset-inline-start`, `text-align: start`) rather than left/right — the whole
page flips on the `dir` attribute alone.

Arabic gets slightly looser line-height and drops the uppercase/letter-spacing
treatments, which are latin-only conventions.

## Placeholders to replace

1. **Logo.** `.logo` is a CSS reconstruction of the wordmark, not the real asset.
   Replace the contents of both `.logo` blocks (header and footer) with
   `<img src="decakila-logo.svg" alt="Decakila">`.
2. **Hero product image.** Drop `052r.<ext>` next to `index.html` — see
   *The hero* below for the extensions tried and why a transparent PNG is worth
   exporting.
3. **Products.** Four dummy cards. Model numbers, specs and the `data-cat`
   filter values are invented.
4. **Contact details.** Phone, email, addresses and opening hours are structurally
   correct but fake.
5. **Branch details.** The seven cities are real — Benghazi, Tripoli, Misrata,
   Al Marj, Al Abyar, Al Bayda, Derna — but addresses and hours are not yet filled in.
6. **Contact form.** Validates in the browser and shows a toast; it does not
   submit anywhere.

## The hero: centred product on brand red

Static and self-contained — no video, no scroll binding, nothing scheduled per
frame. The product sits dead centre with the display wordmark behind it and the
slogan, headline and CTA stacked beneath.

```
.hero                    background: var(--hero-bg)  ← Decakila red, flat
  ├ .hero__eyebrow
  ├ .hero__stage         position: relative; display: grid; place-items: center
  │   ├ .hero__wordmark    absolute, centred — out of flow
  │   ├ .hero__glow        absolute, centred — out of flow
  │   └ .hero__product     the ONLY in-flow item, so it defines the centre
  ├ .hero__lede          slogan · headline · text · white CTA
  └ .hero__bar           three-cell credibility strip
```

Only the product participates in layout. The wordmark is wider than the
container above ~1366px, and as an in-flow grid item it stretched the column and
pushed the product off-centre by half the overflow — 58px at 1440. Out of flow,
the product is centred by the container alone at every width, and the wordmark
is free to bleed toward the viewport edges as display type should. Both are
centred with physical `left`/`top` + `translate`, which is symmetric and so
behaves identically in LTR and RTL.

### The image file

The asset is known only as `052r`. `<picture>`/`<source>` selects by MIME
support rather than by whether a file exists, so it cannot fall back on a 404 —
instead each candidate is probed in turn and the first that decodes wins:

```
052r.png · 052r.webp · 052r.jpg · 052r.jpeg · 052r.avif · 052r
```

Edit `CANDIDATES` in `resolveProductImage()` if the real name differs. If none
resolve, the stage keeps its shape, the wordmark carries the hero on its own,
and the console names every path that was tried.

### The blend, and what it costs

`mix-blend-mode: multiply` computes `backdrop x source` per channel. A **white**
source is the identity for that operation, so a white background multiplied by
anything disappears completely — verified by scanning across the image boundary,
where the largest step is 1/255, i.e. no visible edge at all.

The same maths applies to the product. Against `#E30613` the green and blue
channels are multiplied by roughly 0.02 and 0.07, so a steel-and-glass render
comes out as a red duotone rather than in its own colours. **This is inherent to
multiply on a saturated ground, not a bug.** Two things follow from it:

- **`.hero__glow` is load-bearing, not decoration.** A lighter backdrop is the
  only lever that stops the red crushing the render, so the spotlight behind the
  product buys back colour fidelity at the centre and lets it sink into brand red
  at the edges. Raise the centre stop for more fidelity, lower it for a flatter,
  more graphic look.
- **No drop-shadow under multiply.** A white-background file is opaque across its
  whole rectangle, so `filter: drop-shadow()` traces that *rectangle* rather than
  the product — painting the exact box the blend exists to hide. Measured at a
  12/255 step before removal, 1/255 after.

### Transparency is detected, and preferred

The only way to have a background-free product in *natural colour* on red is a
real alpha channel, which needs no blend at all. So the image is sampled at
runtime and, if any pixel is transparent, it gets `.has-alpha`: the blend drops
to `normal` and the drop-shadow switches on, since it now follows the product's
silhouette instead of its bounding box.

Pixel reading requires a same-origin image, which `file://` does not provide. If
the read is blocked the blend simply stays as `multiply` — the requested
behaviour — and the console says so. Serve over `http://` to get the automatic
upgrade.

**In short: if you can export `052r` as a PNG with transparency, do. It looks
materially better on red and the page will use it automatically.**

### Responsive

The product is sized by `height: clamp(230px, 42vh, 430px)` with
`max-width: min(84vw, 460px)`, so it scales with the viewport and never
overflows. Below 620px the credibility bar drops from three cells to two — the
testimonial steps aside, since three columns do not read at phone width.
Verified centred with no horizontal overflow at 390, 768, 1280 and 1440.

## Accessibility and responsive notes

- Skip link, visible focus rings, `aria-pressed` on the language switch,
  `aria-expanded` on the mobile menu, Escape closes it.
- All interactive targets are at least 44×44 px.
- Red on white is 4.9:1 — sufficient for body text, and body copy uses the dark
  greys anyway.
- Scroll reveals are scoped to `.has-js` so no content is ever hidden if
  scripting fails, and are skipped entirely under `prefers-reduced-motion`.
- Breakpoints at 980 / 860 / 620 / 420 px; verified with no horizontal overflow
  in either direction.
