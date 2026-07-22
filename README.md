# Akshay's Hassio Apps

Personal Home Assistant add-on repository that wraps upstream Docker images as
installable add-ons.

## Add-ons

| Add-on | Description | Port |
|---|---|---|
| [Gokapi](gokapi/) | Lightweight self-hosted file sharing with expiring links | 53842 |
| [BentoPDF](bentopdf/) | Privacy-first PDF toolkit, fully client-side | 3000 |

## Installation

1. In Home Assistant go to **Settings → Add-ons → Add-on Store**.
2. Open the **⋮** menu (top right) → **Repositories**.
3. Add this repository's URL and click **Add**.
4. The add-ons appear in the store under "Akshay's Hassio Apps" — install,
   start, and use the **Open Web UI** button.

Add-ons are built on the Home Assistant host from the upstream image pinned in
each add-on's `build.yaml`, so the first install takes a minute.

## Adding a new app

Copy one of the add-on folders and adjust:

- `config.yaml` — name, slug, version, ports, supported architectures
- `build.yaml` — the upstream image (must be multi-arch or match your HA's
  architecture)
- `Dockerfile` — usually just `FROM ${BUILD_FROM}`; add `ENV`/setup lines if
  the app needs its data redirected to `/data` (the only persistent path)
