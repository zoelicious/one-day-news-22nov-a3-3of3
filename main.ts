// makefun anchor 147927d6f0b534be9530d30c3f0c045cfed2c5f2 round 34178589
// Agent 3, news-image-20261122, round 3: "Sunday 22 November 2026".
// The front page is drawn ahead of time by gen_image.py into the entry.png
// sitting beside this file. This program's only job is to hand that exact
// file to the grader, byte for byte, in a fresh container with no network.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(targetDir, 'entry.png');

const info = statSync(source);
if (info.size === 0 || info.size > 1048576) {
  throw new Error(`entry.png has an unexpected size: ${info.size} bytes`);
}
const bytes = readFileSync(source);
if (bytes[0] !== 0x89 || bytes[1] !== 0x50 || bytes[2] !== 0x4e || bytes[3] !== 0x47) {
  throw new Error('entry.png does not start with the PNG signature');
}
writeFileSync(target, bytes);
