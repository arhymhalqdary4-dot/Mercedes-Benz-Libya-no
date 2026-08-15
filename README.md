# Decakila Libya

A bilingual single-page site for the Decakila appliance range in Libya. Four
views — Home, Products, Services, About us — swap in place with hash routing,
so `#/products?cat=kitchen` is a real, shareable link and browser back/forward
both work.

`index.html` is the whole site: one file, no build step to serve it, no network
calls at runtime. Open it directly or drop it on any static host.

## Building

`index.html` is generated. Edit the sources, not the output.

```
npm install     # Tailwind CSS v4 CLI, dev-only
npm run build   # → index.html + artifact.html
```

| Path                 | What it is                                                    |
| -------------------- | ------------------------------------------------------------- |
| `src/page.html`      | Markup and application script                                 |
| `src/copy.js`        | Every interface string, English and Arabic                    |
| `src/theme.css`      | Tailwind entry: brand tokens, both themes, the curve motif    |
| `data/products.json` | 625 catalogue products extracted from the Decakila price list |
| `assets/`            | Logo, and the white wordmark derived from it                  |
| `build.mjs`          | Compiles Tailwind and inlines CSS, data and logos             |

The build produces the same site in three shapes:

- **`index.html`** — everything inlined. One file, 549 KB, opens by
  double-clicking. Nothing else needed.
- **`artifact.html`** — the same page as a body fragment, for hosts that supply
  their own `<head>`.
- **`local/`** — the split layout: `index.html` (40 KB) beside `styles.css`,
  `products.js`, `copy.js` and `assets/`. Use this one to read or hand-edit the
  page — the catalogue, the stylesheet and the translations stay out of your
  way. Both side scripts load as classic `<script>` tags rather than `fetch()`,
  so the split layout still runs from `file://` with no server.

Both layouts render identically. Pick one — don't mix files between them.

## Catalogue data

`data/products.json` was extracted from the supplied Decakila price-list PDF —
625 items with model code, English and Arabic name, category, and the first
three specifications for each. Categories are derived from the product names:

| Category               | Items |
| ---------------------- | ----: |
| Kitchen Appliances     |   283 |
| Cookware & Kitchenware |   134 |
| Personal Care          |    79 |
| Major Appliances       |    56 |
| Home Care & Cleaning   |    37 |
| Cooling & Heating      |    18 |
| Spare Parts            |    18 |

Wholesale and retail prices appear in the source PDF and were deliberately left
out of the site — the product cards lead to a quote request instead.

Arabic product names are generated from an English→Arabic term map in the
extraction script. They read correctly but are machine-produced; worth a pass by
someone who sells these units daily before launch.

## Language

The globe button in the navbar switches the whole interface between English
(LTR) and Arabic (RTL): copy, layout direction, type stack, and the direction of
the curve motif and chevrons. The choice is remembered between visits, and a
first-time visitor on an Arabic browser lands in Arabic.

All copy lives in `src/copy.js` (`local/copy.js` in the split layout) — `T.en`
and `T.ar` share one set of keys. Add a string to both and tag the element with
`data-i18n="key"`, or read it in a view with `t("key")`. Nothing else needs
touching to change wording, so a translator can work in that one file.

## Design

Brand red `#E10800` is sampled from the logo. Neutrals carry a trace of that red
so greys read as part of the same palette. The logotype's lower edge — a long
S-curve — is the page's structural motif: it closes the hero and every red band,
and mirrors under RTL.

The page follows the viewer's light/dark preference. Every colour is a token
defined in `:root`, redefined for `prefers-color-scheme: dark` and again for an
explicit `data-theme` stamp, so both themes hold whichever way the host renders.

## Before this goes live

1. **Hero video.** The hero `<video>` loads `hero.mp4` from beside `index.html`;
   until that file exists the ambient brand field behind it shows instead, which
   is a deliberate fallback, not a broken state. Drop in a muted H.264 file
   (roughly 8–15 s, under ~5 MB) and it takes over on its own.

2. **Product photography.** Each card requests `images/<MODEL-CODE>.jpg` — for
   example `images/KEEC007B.jpg` — and falls back to the line-art placeholder
   when the file is missing. Add photos named by model code and they appear; no
   code change needed.

3. **Contact details.** The phone number, email, cities and opening hours in the
   footer and quote panel are placeholders.

4. **The quote form.** It validates in-browser and issues a reference number,
   then shows the request for the customer to send on. Nothing is transmitted —
   wire the submit handler in `src/page.html` to your endpoint, WhatsApp Business
   link or CRM.

5. **Commercial claims.** Warranty terms, delivery coverage and service promises
   on the Services and About pages are written as placeholders. Confirm them
   against what the business actually offers.
