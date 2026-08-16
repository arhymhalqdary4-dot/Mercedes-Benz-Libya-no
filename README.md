# Decakila Libya — website

A four-page static site built from the approved UI mockup. No build step, no
dependencies, no framework. Open `index.html` directly or serve the folder with
any static host.

```
index.html     Home — header, hero, trust badges, product grid, promo, footer
products.html  المنتجات — header/footer + dark content placeholder
services.html  الخدمات  — header/footer + dark content placeholder
about.html     من نحن   — header/footer + dark content placeholder
styles.css     the single shared stylesheet
images/        artwork slots — see images/README.md
```

The hamburger toggle is the only script and is inlined at the bottom of each
page, so the four HTML files plus `styles.css` are the whole site.

Two folders from earlier work also sit in the repository and are not part of
the site: `legacy/` (an unrelated Mercedes-Benz page) and `decakila/` (the
first single-file mockup). Delete both if you don't want them.

## Design system

Every colour, font and metric is a CSS custom property at the top of
`styles.css`, so the whole site retones from one block.

| Token | Value | Role |
| --- | --- | --- |
| `--brand-red` | `#e30613` | Decakila red — buttons, hero glow, prices, accents |
| `--brand-red-dark` | `#b4040f` | Button hover |
| `--black` / `--charcoal` | `#050505` / `#0b0b0c` | Page and header ground |
| `--charcoal-2` / `--charcoal-3` | `#111113` / `#17171a` | Trust band, drawer, placeholder panels |
| `--white` | `#ffffff` | Product-grid section and cards |
| `--font-ar` | Cairo → Tajawal | Arabic copy (body default) |
| `--font-en` | Poppins | Latin copy, applied through `.en` |

`--brand-red` is the one value to change if the official brand sheet gives a
different hex; every red on the site derives from it.

Fonts load from Google Fonts. Offline, the stack falls back to the system
sans-serif and nothing else moves.

## Direction

The documents are `lang="ar" dir="rtl"`, so Arabic shapes, wraps and
punctuates correctly, and logical properties (`inset-inline-*`,
`margin-inline`, `padding-inline`) mirror the layout automatically.

The mockup keeps a handful of structural rows in visual left-to-right order —
the logo at the far left of the header, footer columns starting at the left,
product cards reading blender → vacuum. Those rows carry the `.flow-ltr`
utility, which flips the *box order* back to LTR while every text node inside
keeps its own language direction. Remove that class from a row to let it flow
right-to-left instead; nothing else depends on it.

Latin strings inside the RTL document are wrapped in `.en`, which applies the
Poppins stack plus `direction: ltr` and `unicode-bidi: isolate` so mixed
Arabic/English lines like `Home / الرئيسية` never reorder.

## Responsive behaviour

Two breakpoints, matching the three states in the mockup.

- **Desktop (> 1024px)** — full-width hero split into copy and glowing product,
  four-across product grid, three trust badges in a row.
- **Tablet (≤ 1024px)** — the nav collapses into a hamburger drawer, the hero
  tightens, the product grid drops to two columns.
- **Mobile (≤ 640px)** — the hero goes minimalist exactly as drawn: a short
  title, the CTA, then the product. The English lede, tagline and the header's
  Shop Now button are hidden; search, cart and the language switch stay. Trust
  badges stack, the footer becomes a single column.

The `<h1>` swaps its own wording at the mobile breakpoint rather than being
hidden, so the page always exposes one real heading.

## Images

All artwork is referenced but not committed — see `images/README.md` for the
filenames, the box each one renders into, and the recommended source sizes.
Containers are sized independently of the files, so inserting the real images
will not shift the layout.

## Not wired up

The site is presentation only. These are deliberately inert links awaiting a
backend: the search button, the cart (badge is hard-coded to `2`), the `EN / AR`
switch, the add-to-cart buttons, and the customer-service links in the footer.
Product names and prices in the grid are the mockup's copy.
