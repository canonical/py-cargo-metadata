#!/bin/sh
PROJECT_DIR=$(git rev-parse --show-toplevel)

for hook in "$PROJECT_DIR"/git-hooks/*; do
    test ! "$hook" -ef "$0" || continue
    ln -s "$hook" "$PROJECT_DIR/.git/hooks/$(basename "$hook")" 2>/dev/null ||
        echo "hook $(basename "$hook") already exists"
done
