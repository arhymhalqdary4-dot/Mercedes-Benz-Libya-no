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
2. **Hero video.** Drop `hero.mp4` next to `index.html`. It has one hard
   encoding requirement — see *Scroll-bound video scrubbing* below.
3. **Products.** Four dummy cards. Model numbers, specs and the `data-cat`
   filter values are invented.
4. **Contact details.** Phone, email, addresses and opening hours are structurally
   correct but fake.
5. **Branch details.** The seven cities are real — Benghazi, Tripoli, Misrata,
   Al Marj, Al Abyar, Al Bayda, Derna — but addresses and hours are not yet filled in.
6. **Contact form.** Validates in the browser and shows a toast; it does not
   submit anywhere.

## Scroll-bound video scrubbing

The hero binds `hero.mp4`'s `currentTime` to scroll position, so the blender
render advances frame-by-frame as you scroll down and reverses as you scroll up.

### Structure

```
.hero-track      height: var(--hero-scroll)   ← supplies the scroll distance
  └ .hero       position: sticky; top: 0     ← stays pinned while the page moves
      ├ .hero__video    pinned behind, object-fit: cover
      ├ .hero__scrim    keeps the copy legible over any frame
      └ .container      the copy, z-index 3
```

`--hero-scroll` (default `300vh`) is the only knob for how long the scrub lasts:
one viewport of pinning plus two of scrubbing. Raise it for a slower, more
deliberate scrub; lower it to get through the clip faster.

### How it stays smooth

- The scroll listener is passive and does nothing but wake the rAF loop. All
  reads and writes happen inside one frame callback, so scrolling never forces
  a synchronous layout.
- Layout metrics are measured once and re-measured only on resize — never per
  frame.
- The played time *eases* toward the scroll target rather than snapping to it.
  That easing is what turns a jumpy seek into a glide, and it makes reverse
  scrubbing feel identical to forward.
- Seeks are skipped while a previous seek is in flight, so a fast flick queues
  one seek instead of fighting the decoder for dozens.
- The loop only runs while the hero is on screen, and parks itself as soon as
  the eased time settles — measured at 0 rAF calls per second when idle.

### The one hard requirement: the file must be seekable

Scroll scrubbing is seeking, and a video can be *fully downloaded and still
refuse to seek* if it carries no seek index. When that happens every write to
`currentTime` is silently dropped and the hero freezes on frame one. Export with
the index at the front:

```bash
ffmpeg -i source.mov -c:v libx264 -pix_fmt yuv420p \
       -movflags +faststart -an hero.mp4
```

Also make sure the host answers HTTP range requests (almost all do; some
naive static servers do not).

Two further encoding notes:

- **Keyframes.** Seeking lands on the nearest keyframe, so a clip with the
  default one every ~250 frames will scrub in visible steps. Add `-g 10` or
  lower for dense keyframes — it inflates the file, which is the trade you want
  here. `-g 1` (all keyframes) is smoothest and largest.
- **Size.** The whole clip must download before it can scrub cleanly. Keep it
  short and modest in resolution; 1280×720 is plenty behind a scrim.

The page detects the unseekable case: if the file finishes buffering and still
cannot seek, it collapses to a normal one-screen hero and logs a console warning
explaining the fix, rather than leaving a frozen frame above three screens of
dead scroll.

### Degradation

| Situation | Behaviour |
| --- | --- |
| `hero.mp4` missing or errors | Track collapses to a normal hero over the gradient; no dead scroll |
| File loads but is not seekable | Same collapse, plus a console warning naming the fix |
| Still buffering | Seeks retry automatically as data arrives — it catches up on its own |
| `prefers-reduced-motion` | No scrubbing; one representative frame, shown statically |
| Hero scrolled past quickly | Snaps to the boundary frame instead of freezing mid-ease |

### Bilingual

Scrubbing is driven by vertical scroll, so it is direction-agnostic and works
identically in both languages. Two details are handled explicitly: the video
itself does **not** mirror in RTL (it is a product render, not an ornament,
unlike the swoosh), and the scrim's directional wash flips to sit under the
copy on whichever side it lands. Switching language mid-scrub keeps the current
position.

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
