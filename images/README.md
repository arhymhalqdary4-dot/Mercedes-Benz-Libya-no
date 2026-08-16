# Image slots

Drop the real artwork here using exactly these filenames — the markup already
points at them and every container is sized, so nothing in the CSS needs to
change when the files land.

| File | Used on | Rendered box | Recommended source |
| --- | --- | --- | --- |
| `logo.png` | header, all pages | 132 × 46 px, `object-fit: contain` | the red logo lockup, transparent PNG or SVG, ~400 × 140 px |
| `mixer.png` | hero, `index.html` | square, up to 370 px | hero product cut-out on transparency, ≥ 900 × 900 px |
| `blender.png` | product card 1 | 210 px tall box | product cut-out on transparency or white, ~800 × 800 px |
| `air-fryer.png` | product card 2 | 210 px tall box | same |
| `microwave.png` | product card 3 | 210 px tall box | same |
| `vacuum.png` | product card 4 | 210 px tall box | same |
| `promo-kitchen.jpg` | promo banner | full-bleed, `object-fit: cover` | dark kitchen scene, ≥ 1920 × 900 px, subject on the right |
| `favicon.png` | browser tab | 32 × 32 px | red mark on transparency |

Notes

- Product shots want a **transparent background**. The hero ring and the white
  product grid both read best with the appliance floating, exactly as in the
  approved mockup.
- The promo photo is darkened by a gradient laid over it, so a mid-exposure
  photo works better than an already-dark one.
- Every `<img>` carries Arabic alt text; update it if a slot is filled with a
  different product.
