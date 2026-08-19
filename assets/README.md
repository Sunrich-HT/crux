# Brand Assets

The source mark in `crux-arena-original.jpg` was generated with Flux through Arena on 2026-08-19. It was then color-normalized and composed into the repository banner and social preview with `scripts/build_brand_assets.py`.

## Generation prompt

```text
Design an original flat vector logo mark for Crux, an evidence-governed AI thinking partner. Show two opposing reasoning paths converging at one decisive pivot and resolving into one clear forward direction. Single centered geometric symbol, strong silhouette, generous white space, readable at 32px. Deep teal #0F766E, signal coral #E4573D, charcoal #172126, off-white background. No text or letters. No gradients, 3D, shadows, mockup, watermark, brain, lightbulb, scales, chat bubble, magnifying glass, or maze.
```

## Rebuild

```bash
python -m pip install pillow
python scripts/build_brand_assets.py
```

Generated outputs:

- `crux-logo-1024.png`: cleaned square project mark;
- `readme-banner.png`: 1600 x 640 README cover;
- `social-preview.png`: 1280 x 640 GitHub social preview;
- `skills/crux/assets/`: skill UI icon and large logo.

The Crux project logo and derived brand assets are distributed under the repository's MIT License.
