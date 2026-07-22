ARG BUILD_FROM
FROM ${BUILD_FROM}

# Persist Stirling's settings in Home Assistant's per-add-on /data volume.
# run.sh creates /data/configs before the stock init so the symlink resolves.
RUN rm -rf /configs && ln -s /data/configs /configs
COPY run.sh /run-addon.sh
RUN chmod +x /run-addon.sh
ENTRYPOINT ["tini", "--", "/run-addon.sh"]

# No login page — the add-on is only reachable on the local network
ENV SECURITY_ENABLELOGIN=false
