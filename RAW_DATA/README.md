# RAW_DATA

Centralized, **local-only** storage for original source material (lecture PDFs, ZIP bundles, raw exports).

- Layout: `RAW_DATA/<subject>/<LECxx>/<original files>`.
- Everything here except this README is excluded by `.gitignore`; original material is never committed or published unless its license is confirmed and a separate approved Issue says so.
- Originals are read-only. Never edit, repack or overwrite them; extract to a scratch directory and record SHA-256 values in the Issue/Result instead.
- Derived, approved teaching Markdown lives under `docs/subjects/`; per-Issue relearning lists live under `RELEARNING_SUPPLEMENTS/ISSUE-<number>/`.
