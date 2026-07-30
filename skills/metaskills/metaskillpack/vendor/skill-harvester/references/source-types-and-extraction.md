# Source Types and Extraction

## Local codebases

Treat the current codebase as explicit only when the user identifies it as source. Begin with repository instructions, manifests, README files, architecture docs, source entry points, tests, and relevant paths. Preserve dirty worktrees and avoid generated, vendored, cached, dependency, build, and secret files unless required.

## Plain text and source code

Read Markdown, text, JSON, YAML, TOML, CSV, HTML, logs, and source code directly with bounded size. Preserve path, hash, encoding, heading or symbol locator, and extraction failures.

## Container documents

Prefer purpose-built artifact tools for PDF, DOCX, spreadsheets, and presentations. If unavailable, `scripts/extract_documents.py` can extract text from plain formats, DOCX, ODT, PPTX, HTML, and RTF; PDF extraction uses `pypdf` or `pdftotext` when available. Old binary Office files and image-only PDFs require dedicated conversion or OCR.

Never treat extraction success as semantic correctness. For PDF and rendered documents, preserve page/layout caveats and perform visual inspection when layout matters.

## Mixed directories

Inventory before extraction, classify each file, exclude unsupported binaries explicitly, and write normalized text only to an authorized separate destination. Do not silently flatten duplicate filenames or lose source mapping.
