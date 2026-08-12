/**
 * Build: compiles Tailwind against src/page.html and inlines the stylesheet,
 * the catalogue data and the logo assets into a single self-contained
 * index.html. No runtime dependencies ship with the page.
 *
 *   npm install && node build.mjs
 */
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
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

const dataUri = (file, mime) =>
  `data:${mime};base64,${readFileSync(join(root, file)).toString("base64")}`;

const css = readFileSync(cssOut, "utf8");
const data = JSON.stringify(JSON.parse(readFileSync(join(root, "data/products.json"), "utf8")));

const body = readFileSync(join(root, "src/page.html"), "utf8")
  .replace("{{TAILWIND_CSS}}", () => css)
  .replace("{{DATA}}", () => data)
  .replaceAll("{{LOGO_BLOCK}}", () => dataUri("assets/logo.png", "image/png"))
  .replaceAll("{{LOGO_WHITE}}", () => dataUri("assets/logo-wordmark-white.png", "image/png"));

/* index.html — the site. lang/dir are rewritten by the language switch.
   src/page.html is authored as head-matter up to </style>, then page body. */
const split = body.indexOf("</style>") + "</style>".length;
const page = `<!doctype html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
${body.slice(0, split).trim()}
</head>
<body>
${body.slice(split).trim()}
</body>
</html>
`;
writeFileSync(join(root, "index.html"), page);

/* artifact.html — same page as a body fragment, for hosts that supply their
   own document shell. */
writeFileSync(join(root, "artifact.html"), body);

rmSync(tmp, { recursive: true, force: true });

const kb = (n) => (n / 1024).toFixed(0) + " KB";
console.log(`· css   ${kb(css.length)}`);
console.log(`· data  ${kb(data.length)} · ${JSON.parse(data).items.length} products`);
console.log(`· wrote index.html + artifact.html (${kb(page.length)})`);
