/**
 * Build. Compiles Tailwind against src/page.html and emits two shapes of the
 * same site:
 *
 *   index.html      everything inlined — one file, opens by double-click
 *   artifact.html   the same, as a body fragment for hosts with their own head
 *   local/          index.html + styles.css + products.js + assets/
 *                   the split layout: index.html small enough to read, paste
 *                   and hand-edit; the catalogue and stylesheet sit beside it
 *
 * The split build loads products.js as a classic script, not fetch(), so it
 * works from file:// with no server.
 *
 *   npm install && node build.mjs
 */
import { execFileSync } from "node:child_process";
import {
  readFileSync, writeFileSync, mkdtempSync, rmSync, mkdirSync, copyFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const tmp = mkdtempSync(join(tmpdir(), "decakila-"));
const cssOut = join(tmp, "app.css");

console.log("· compiling Tailwind");
execFileSync(
  process.execPath,
  [
    join(root, "node_modules/@tailwindcss/cli/dist/index.mjs"),
    "--input", join(root, "src/theme.css"),
    "--output", cssOut,
    "--minify",
  ],
  { stdio: "inherit", cwd: root }
);

const css = readFileSync(cssOut, "utf8");
const source = readFileSync(join(root, "src/page.html"), "utf8");
const data = JSON.stringify(
  JSON.parse(readFileSync(join(root, "data/products.json"), "utf8"))
);
const dataUri = (file, mime) =>
  `data:${mime};base64,${readFileSync(join(root, file)).toString("base64")}`;

/** Fill the template. `mode` picks inlined assets or files beside the page. */
function render(mode) {
  const inline = mode === "inline";
  return source
    .replace("{{STYLES}}", () =>
      inline
        ? `<style>${css}</style>`
        : `<link rel="stylesheet" href="styles.css" />`)
    .replace("{{DATA_TAG}}", () =>
      inline ? "" : `<script src="products.js"></script>`)
    .replace("{{DATA}}", () => (inline ? data : "window.DECAKILA_DATA"))
    .replaceAll("{{LOGO_BLOCK}}", () =>
      inline ? dataUri("assets/logo.png", "image/png") : "assets/logo.png")
    .replaceAll("{{LOGO_WHITE}}", () =>
      inline
        ? dataUri("assets/logo-wordmark-white.png", "image/png")
        : "assets/logo-wordmark-white.png");
}

/** Wrap a filled template in a complete HTML document. */
function document_(filled) {
  const marker = "<!--/head-->";
  const cut = filled.indexOf(marker);
  const head = filled.slice(0, cut).trim();
  const body = filled.slice(cut + marker.length).trim();
  return `<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
${head}
</head>
<body>
${body}
</body>
</html>
`;
}

const inlined = render("inline");
const page = document_(inlined);
writeFileSync(join(root, "index.html"), page);
writeFileSync(join(root, "artifact.html"), inlined.replace("<!--/head-->", ""));

const local = join(root, "local");
mkdirSync(join(local, "assets"), { recursive: true });
mkdirSync(join(local, "images"), { recursive: true });
const localPage = document_(render("split"));
writeFileSync(join(local, "index.html"), localPage);
writeFileSync(join(local, "styles.css"), css);
writeFileSync(
  join(local, "products.js"),
  `/* Decakila catalogue — generated from the price-list PDF by\n   tools/extract-catalogue.py. Loaded before index.html's script. */\nwindow.DECAKILA_DATA = ${data};\n`
);
copyFileSync(join(root, "assets/logo.png"), join(local, "assets/logo.png"));
copyFileSync(
  join(root, "assets/logo-wordmark-white.png"),
  join(local, "assets/logo-wordmark-white.png")
);
writeFileSync(
  join(local, "images/README.txt"),
  "Product photos go here, named by model code:\n\n  KEEC007B.jpg\n  KEJB001W.jpg\n  ...\n\nAny card whose photo is missing keeps its line-art placeholder.\n"
);

rmSync(tmp, { recursive: true, force: true });

const kb = (n) => (n / 1024).toFixed(0) + " KB";
console.log(`· css   ${kb(css.length)}`);
console.log(`· data  ${kb(data.length)} · ${JSON.parse(data).items.length} products`);
console.log(`· wrote index.html + artifact.html (${kb(page.length)})`);
console.log(`· wrote local/index.html (${kb(localPage.length)}) + styles.css + products.js`);
