/**
 * Packages the built site into dist/decakila-website.zip.
 *
 *   npm run package        (runs the build first)
 *
 * Zip layout — both ways of running the same site, plus the sources:
 *
 *   decakila-website/
 *     README.md            what to do with everything here
 *     website/             the working copy: index.html + styles.css +
 *                          products.js + copy.js + assets/ + images/
 *     single-file/         index.html with everything inlined, nothing beside it
 *     source/              src/, data/, assets/, tools/, build.mjs — rebuilds both
 */
import { execFileSync } from "node:child_process";
import { cpSync, mkdirSync, rmSync, writeFileSync, readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const base = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(base, "dist");
const stage = join(dist, "decakila-website");

if (!existsSync(join(base, "local/index.html"))) {
  console.error("run `npm run build` first — local/ is missing");
  process.exit(1);
}

rmSync(dist, { recursive: true, force: true });
mkdirSync(stage, { recursive: true });

/* 1 — the working copy */
cpSync(join(base, "local"), join(stage, "website"), { recursive: true });

/* 2 — the single-file build */
mkdirSync(join(stage, "single-file/images"), { recursive: true });
cpSync(join(base, "index.html"), join(stage, "single-file/index.html"));
cpSync(
  join(base, "local/images/README.txt"),
  join(stage, "single-file/images/README.txt")
);

/* 3 — sources, so the whole thing can be rebuilt */
const src = join(stage, "source");
mkdirSync(src, { recursive: true });
for (const p of ["src", "data", "assets", "tools"]) {
  cpSync(join(base, p), join(src, p), { recursive: true });
}
for (const f of ["build.mjs", "package.json", "README.md"]) {
  cpSync(join(base, f), join(src, f));
}

writeFileSync(join(stage, "README.md"), readFileSync(join(base, "tools/zip-readme.md")));

execFileSync("zip", ["-qr", "decakila-website.zip", "decakila-website"], { cwd: dist });
rmSync(stage, { recursive: true, force: true });

const bytes = readFileSync(join(dist, "decakila-website.zip")).length;
console.log(`· wrote dist/decakila-website.zip (${(bytes / 1024).toFixed(0)} KB)`);
