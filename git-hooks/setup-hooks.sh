#!/bin/sh
PROJECT_DIR=$(git rev-parse --show-toplevel)

for hook in "$PROJECT_DIR"/git-hooks/*; do
    test ! "$hook" -ef "$0" || continue
    ln -st "$PROJECT_DIR"/.git/hooks "$hook" 2>/dev/null ||
        echo "hook $(basename "$hook") already exists"
done
