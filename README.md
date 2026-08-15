# ديكاكيلا ليبيا — Decakila Libya

Single-page marketing layout for Decakila Libya, built from the approved UI/UX
mockup. One self-contained file, `index.html` — plain HTML5, plain CSS, and one
small vanilla-JS block. No build step and no framework.

Open the file directly in a browser, or serve the folder with any static host.

## Layout

Arabic-first, `dir="rtl"` on `<html>`. Everything that has a side uses CSS
logical properties (`inset-inline-start`, `padding-inline-end`, `margin-inline`),
so flipping the document to `dir="ltr"` mirrors the whole page correctly without
touching the stylesheet.

Sections, top to bottom:

| # | Section | Theme |
|---|---------|-------|
| 03 | Header — red curved logo plate, centred nav with active underline, CTA | dark, transparent → solid on scroll |
| 04 | Hero — headline, two CTAs, product inside a glowing red ring, slider dots | dark gradient |
| 05 | Trust bar — five feature columns with line-art icons | white |
| 06 | Products — `منتجات مميزة` heading + four-column card grid | light gray |
| 07 | Promo banner — appliance line-up, copy, red CTA, line-art house | dark, rounded |
| 08 | Stats — 7+ / 25K+ / 500+ / 12+ / 4.8 with counting animation | white |
| 09 | Footer — brand, links, hours, contact, socials | black |

Section numbers in the table match the comment banners in the CSS and the JS, so
searching for `06 PRODUCTS` lands on the markup, the styles, and any behaviour
for that block.

## Colours

All tokens live in `:root` at the top of the stylesheet. The brand red is
`--red: #e30613`; `--red-dark` is the hover state and `--red-glow` drives the
hero aura. Changing the two red values re-skins the whole page.

## Images

Every appliance is a placeholder path under `images/`. Drop real files in with
these names and nothing else needs changing — sizes, aspect ratios, and
positioning are all handled in CSS:

```
images/hero-stand-mixer.png      hero, slide 1        transparent PNG, ~1000×1000
images/hero-coffee-maker.png     hero, slide 2        transparent PNG, ~1000×1000
images/hero-vacuum.png           hero, slide 3        transparent PNG, ~1000×1000
images/hero-part-whisk.png       floating accessory   transparent PNG, ~300×300
images/hero-part-hook.png        floating accessory   transparent PNG, ~300×300
images/hero-part-beater.png      floating accessory   transparent PNG, ~300×300
images/promo-appliances.png      promo banner         transparent PNG, ~1240×720
images/products/blender.png      product card         transparent PNG, ~800×800
images/products/coffee-maker.png product card         transparent PNG, ~800×800
images/products/air-fryer.png    product card         transparent PNG, ~800×800
images/products/vacuum.png       product card         transparent PNG, ~800×800
```

Transparent PNGs on a dark backdrop are what the design assumes. Until the files
exist, each `<img>` renders as a soft gray plate (`img.ph`) so the layout stays
readable instead of showing broken-image icons.

## Behaviour (`<script>` at the end of the file)

1. Header turns solid and shrinks past 40px of scroll.
2. Mobile nav — the hamburger appears at ≤980px and closes on link tap.
3. Scroll spy — the nav underline follows the section in view.
4. Hero slider — three slides on a 6s loop, clickable dots, pauses when the tab
   is hidden. Copy and image for each slide are in the `slides` array; edit
   there, not in the markup.
5. Reveal on scroll via `IntersectionObserver`, staggered per row.
6. Stat counters animate once when the strip scrolls into view.
7. Add-to-cart buttons flip to a checkmark for 1.6s. This is UI feedback only —
   there is no cart state or backend behind it yet.
8. Back-to-top button appears past 600px.

Everything degrades gracefully: with `prefers-reduced-motion: reduce`, all
animation is disabled, reveals start visible, and the slider stops auto-playing.

## Responsive breakpoints

- **≤1080px** — nav tightens, the promo house graphic is dropped.
- **≤980px** — hero stacks with the product on top, nav collapses to a drawer,
  trust bar goes 3-up, products 2-up, footer 2-up.
- **≤620px** — trust bar and stats go 2-up, promo perks stack, hero buttons go
  full width, footer becomes a single column.

## Before this goes live

The phone number, email, address, working hours, prices, and the figures in the
stats strip are placeholders from the mockup — swap them for real values. The
social links in the footer point at `#`.

## Type

Cairo, loaded from Google Fonts in `<head>`. To self-host, drop the woff2 files
next to the page and replace the `<link>` with `@font-face` rules — the
`font-family` on `body` already falls back to Tajawal and then the system UI
stack, so a failed font load never breaks the Arabic rendering.

---

The earlier Mercedes-Benz Libya landing page that lived in this repository has
been moved to [`mercedes-libya/`](mercedes-libya/) — it is unchanged.
