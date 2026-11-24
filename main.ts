// Entry point for the v3 news-image entry.
// Copies the pre-rendered front page (entry.png, drawn by render.py)
// into the grader's output directory, after checking the file is a real
// PNG and small enough for the bounty cap. Node standard library only.

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// The bounty caps the image at 1 MiB; a bigger file would fail the gate.
const MAX_BYTES = 1024 * 1024;

function abort(message) {
  console.error("main.ts: " + message);
  process.exit(1);
}

function main() {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");

  if (!existsSync(source)) {
    abort("entry.png is missing next to main.ts");
  }
  const picture = readFileSync(source);

  if (picture.length > MAX_BYTES) {
    abort("entry.png is " + picture.length + " bytes, over the 1 MiB cap");
  }
  if (picture.subarray(0, PNG_MAGIC.length).compare(PNG_MAGIC) !== 0) {
    abort("entry.png does not start with the PNG magic bytes");
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const target = join(outDir, "entry.png");
  writeFileSync(target, picture);

  const fingerprint = createHash("sha256").update(picture).digest("hex");
  console.log(
    "main.ts: wrote " + target + " (" + picture.length + " bytes, sha256 " +
    fingerprint + ")",
  );
}

main();
