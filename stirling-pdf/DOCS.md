# Stirling PDF

[Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) is a locally
hosted web application offering a large set of PDF operations: merge, split,
convert, OCR, compress, sign, redact, and more. This add-on uses the "fat"
image variant, which bundles all optional features (LibreOffice conversions,
OCR, etc.), so the first install downloads a large image.

## Usage

1. Start the add-on.
2. Open `http://<home-assistant-ip>:2080` (or use the **Open Web UI** button).

## Data

Application settings (`/configs`) are stored in the add-on's persistent
`/data` volume and survive restarts and updates. PDF processing itself is
transient — uploaded files are not kept after processing.

## Updating

The add-on version tracks the upstream Stirling PDF release pinned in
`build.yaml`. To update, bump the tag in `build.yaml` and the `version` in
`config.yaml` in the repository, then refresh the add-on store.
