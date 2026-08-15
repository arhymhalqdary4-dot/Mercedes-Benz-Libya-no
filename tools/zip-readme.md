# Decakila Libya — website

A bilingual (English / Arabic) four-page site for the Decakila appliance range:
Home, Products, Services, About us. All 625 products from the price-list PDF are
in it, with filtering and search. No server, no build step, no internet needed
to run it — open the file and it works.

This zip contains the same site twice, plus the sources.

---

## Start here: `website/`

This is the copy to work with.

```
website/
├── index.html      the page
├── styles.css      compiled stylesheet
├── products.js     the 625-product catalogue
├── copy.js         every word of text, English and Arabic
├── assets/         logo files
└── images/         your product photos go here
```

Open `website/index.html` in any browser. To publish, upload the whole
`website/` folder to any static host.

### Add your video

Put `hero.mp4` directly inside `website/`, next to `index.html`. That's all —
the hero picks it up automatically. Until it's there you'll see the red brand
field instead, which is the intended fallback, not a fault.

A muted H.264 file, roughly 8–15 seconds, under about 5 MB works best.

If your video's subject ends up behind the headline, open `styles.css`, search
for `--hero-shift`, and change `11%` to `0%` (leave the framing alone) or `-11%`
(push it the other way).

### Add your product photos

Drop them into `website/images/`, named by model code:

```
website/images/KEEC007B.jpg
website/images/KEJB001W.jpg
```

The model code is printed on every product card. Any product without a photo
keeps its line-art placeholder, so you can add them a few at a time.

### Change wording

All text lives in `copy.js` — English in `T.en`, Arabic in `T.ar`, sharing the
same keys. It contains no code, so anyone can edit it safely. Phone number,
email, cities and opening hours are in `index.html`, in the footer.

---

## `single-file/`

The identical site as one self-contained `index.html` — stylesheet, catalogue,
text and logos all inside that one file. Handy for emailing, or for a host that
only accepts a single page.

`hero.mp4` and `images/` work exactly the same way: put them beside the file.

Use one folder or the other. Don't mix files between them.

---

## `source/`

Everything the two builds are generated from.

```
cd source
npm install
npm run build
```

That regenerates both layouts: `source/index.html` (single-file) and
`source/local/` (the split copy). Edit `src/page.html` for markup and behaviour,
`src/copy.js` for wording, `src/theme.css` for colours and the design tokens.

`source/tools/extract-catalogue.py` is the script that read the Decakila
price-list PDF and produced `data/products.json`. Re-run it against a newer
price list to refresh the catalogue:

```
pip install pypdf
python3 tools/extract-catalogue.py new-catalogue.pdf data/products.json
```

`source/README.md` has the full technical detail.

---

## Before this goes public

1. **Contact details** — the phone number, email, cities and opening hours are
   placeholders.
2. **The quote form** — it validates the customer's details and issues a
   reference number, then shows them the request to send on. Nothing is
   transmitted anywhere yet; it needs connecting to an email address, a WhatsApp
   Business link or your CRM.
3. **Warranty and service claims** — the promises written on the Services and
   About pages are plausible placeholders. Check them against what the business
   actually offers.
4. **Arabic product names** — machine-generated from the English catalogue.
   They read correctly, but someone who sells these units daily should skim
   them before launch.
5. **Prices** — the wholesale and retail columns in the source PDF were left out
   on purpose. Products lead to a quote request instead.
