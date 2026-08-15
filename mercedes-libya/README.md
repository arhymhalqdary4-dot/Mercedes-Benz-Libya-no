# Mercedes-Benz Libya — landing application

A single self-contained file, `index.html`. No build step, no dependencies, no
network calls. Open it directly, or serve the directory with any static host.

Four views (Home, Models, Services, About Us) swap in place with hash routing,
so browser back/forward and deep links such as `#/models` both work.

## Bilingual

One button in the header switches the whole application between Arabic (RTL)
and English (LTR): text, layout direction, type stack, per-script letter-spacing,
and the direction the vehicle silhouettes face. The choice is remembered between
visits.

All copy lives in the `T` object at the top of the script — `T.en` and `T.ar`
share one set of keys. Adding a string means adding it to both and tagging the
element with `data-i18n="key"`.

## Before this goes live

Two things in the file are placeholders and need real values:

1. **Hero video.** The `<source>` in `#heroVideo` points at the URL supplied for
   the build, which is not publicly reachable — the hero currently renders its
   ambient fallback instead. Replace the `src` with a hosted MP4 (H.264, muted,
   roughly 8–15 s, ideally under 5 MB) and the fallback stands down on its own.
   Nothing else needs changing; the detection is automatic.

2. **Contact details.** Phone numbers, addresses, map coordinates and opening
   hours in the `LOCATIONS` array — and the numbers in the services panel and
   footer — are structurally correct but invented. Swap them for the real ones.

Vehicle figures are manufacturer WLTP/EU specification. Prices are indicative
landed estimates in USD before duty and registration, and are labelled as such
in the footer.

## Booking form

The appointment modal validates in-browser and issues a reference number. It has
no backend — nothing is transmitted anywhere, and the form says so. Point the
`submit` handler in section 13 of the script at your endpoint to make it live.

## Notes on the build

- Typefaces (Archivo, IBM Plex Sans Arabic, IBM Plex Mono) are subset to the
  glyphs actually used and embedded as data URIs, so the page renders identically
  offline and behind a strict content-security policy.
- The utility classes at the top of the stylesheet deliberately mirror Tailwind's
  names. Dropping this markup into a Tailwind project means deleting that block;
  the class names resolve against the framework unchanged.
- Vehicle imagery is drawn as inline SVG — one silhouette per body style — rather
  than loaded from files.
- Respects `prefers-reduced-motion`; all interactive elements are keyboard
  reachable with a visible focus state.
