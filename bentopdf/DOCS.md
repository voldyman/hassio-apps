# BentoPDF

[BentoPDF](https://github.com/alam00000/bentopdf) is a privacy-first PDF
toolkit: merge, split, compress, convert, sign, and edit PDFs. Everything runs
client-side in your browser — files never leave your machine; this add-on only
serves the static web app.

## Usage

1. Start the add-on.
2. Open `http://<home-assistant-ip>:3000` (or use the **Open Web UI** button).

The add-on is stateless — there is nothing to configure and no data is stored
on the server.

## Updating

The add-on version tracks the upstream BentoPDF release pinned in `build.yaml`.
To update, bump the tag in `build.yaml` and the `version` in `config.yaml` in
the repository, then refresh the add-on store.
