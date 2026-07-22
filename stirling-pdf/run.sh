#!/bin/bash
# Ensure the persistent config dir exists before Stirling starts,
# so the /configs -> /data/configs symlink resolves.
mkdir -p /data/configs
exec /scripts/init.sh "$@"
