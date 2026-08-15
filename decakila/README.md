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
2. **Hero video.** `<video id="hero-video">` has no `<source>` yet. Uncomment the
   line inside it and point at your MP4 (H.264, muted, ~8–15 s). It fades in on
   its own `playing` event; until then the branded gradient stands in, so there
   is no broken state at any point.
3. **Products.** Four dummy cards. Model numbers, specs and the `data-cat`
   filter values are invented.
4. **Contact details.** Phone, email, addresses and opening hours are structurally
   correct but fake.
5. **Branch details.** The seven cities are real — Benghazi, Tripoli, Misrata,
   Al Marj, Al Abyar, Al Bayda, Derna — but addresses and hours are not yet filled in.
6. **Contact form.** Validates in the browser and shows a toast; it does not
   submit anywhere.

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
