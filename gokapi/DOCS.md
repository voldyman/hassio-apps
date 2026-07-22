# Gokapi

[Gokapi](https://github.com/Forceu/Gokapi) is a lightweight self-hosted file
sharing server: upload files, get expiring download links, no accounts needed
for recipients.

## First-time setup

1. Start the add-on.
2. Open `http://<home-assistant-ip>:53842/setup` in your browser and follow
   the setup wizard to create the admin account.
3. After setup, the admin UI lives at `http://<home-assistant-ip>:53842/admin`
   (the **Open Web UI** button takes you to the main page).

## Data

All configuration and uploaded files are stored in the add-on's persistent
`/data` volume, so they survive restarts, updates, and rebuilds. They are
included in Home Assistant backups — note that large uploads will grow your
backup size.

## Updating

The add-on version tracks the upstream Gokapi release pinned in `build.yaml`.
To update, bump the tag in `build.yaml` and the `version` in `config.yaml` in
the repository, then refresh the add-on store.
