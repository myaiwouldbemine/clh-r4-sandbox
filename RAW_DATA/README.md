# RAW_DATA

Centralized, **local-only** storage for original source material (lecture PDFs, ZIP bundles, raw exports) and ChatGPT + Human generated teaching bundles.

Workflow context: [Learning-to-Publishing Workflow（教材製作與發布流程）](../README.md#learning-to-publishing-workflow) in the root README.

## Layout

```text
RAW_DATA/<subject>/<unit>/
├── ORIGINAL/    # original source files, e.g. lec08.pdf
└── GENERATED/   # ChatGPT + Human outputs: PDF / HTML / MD / ZIP, e.g. LEC08_FULL_DRAFT.zip
```

Example: `RAW_DATA/operating-systems/LEC08/ORIGINAL/lec08.pdf` and `RAW_DATA/operating-systems/LEC08/GENERATED/LEC08_FULL_DRAFT.zip`. Earlier single-layer `<subject>/<LECxx>/<files>` placements are legacy; place new material in `ORIGINAL/` or `GENERATED/`.

## Rules

- **Git exclusion:** everything here except this README is excluded by `.gitignore` (`/RAW_DATA/**`). Original PDFs and generated ZIPs are never committed or published unless their license is confirmed and a separate approved Issue says so.
- **Read-only:** never edit, repack or overwrite files in `ORIGINAL/` or `GENERATED/`. Extract to a scratch directory instead.
- **SHA-256:** record the SHA-256 of each original and generated file in the Learning Record or Engineering Task Result.
- **Versioning:** a revised bundle is a new file (for example a new name or version suffix) with its own SHA-256; do not overwrite earlier versions.
- **License:** note the license or usage terms of each original source in the Learning Record before any publication decision.
- **Local backup:** because Git does not hold these files, keep your own local backup (for example an external drive or private storage) of `RAW_DATA/`.
- **Derived content:** approved teaching Markdown lives under `docs/subjects/`; per-Issue relearning lists live under `RELEARNING_SUPPLEMENTS/ISSUE-<number>/`; engineering evidence lives under `records/ISSUE-<number>/`.
