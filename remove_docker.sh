#!/bin/bash

echo "🔍 Searching for Docker-related files..."

DOCKER_PATHS=(
    "/Applications/Docker.app"
    "$HOME/Library/Containers/com.docker.docker"
    "$HOME/Library/Application Support/Docker"
    "$HOME/Library/Group Containers/group.com.docker"
    "$HOME/Library/Preferences/com.docker.docker.plist"
    "$HOME/Library/Saved Application State/com.docker.docker.savedState"
    "/Library/PrivilegedHelperTools/com.docker.*"
    "$HOME/.docker"
    "/usr/local/bin/docker"
    "/usr/local/bin/docker-compose"
    "/Volumes/Server/com.docker.docker"
    "/Volumes/Server/Docker_Images"
)

for path in "${DOCKER_PATHS[@]}"; do
    if [ -e "$path" ]; then
        echo "🗑️ Deleting: $path"
        sudo rm -rf "$path"
    fi
done

echo "🧹 Flushing system cache..."
sudo mdutil -E /

echo "✅ Docker cleanup complete."
