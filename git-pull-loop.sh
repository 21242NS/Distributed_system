#!/bin/sh

set -u

git config --global --add safe.directory /app

while true; do
    echo "[git-puller] Checking for updates..."
    branch="${GIT_BRANCH:-$(git branch --show-current)}"
    git pull --ff-only origin "$branch" || \
        echo "[git-puller] Pull failed; retrying later"
    sleep "${PULL_INTERVAL:-30}"
done