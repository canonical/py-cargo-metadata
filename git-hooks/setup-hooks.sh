#!/bin/sh

set -eu

PROJECT_DIR=$(git rev-parse --show-toplevel)
SETUP_HOOKS_DIR=$(dirname "$(realpath "$0")")
GIT_HOOKS_DIR=$PROJECT_DIR/.git/hooks

for hook in "$SETUP_HOOKS_DIR/*; do
    test ! "$hook" -ef "$0" || continue # this script isn't a hook
    hookname=$(basename "$hook")
    destfile=$GIT_HOOKS_DIR/$hookname
    test ! "$hook" -ef "$destfile" || continue # hook already linked
    ln -s "$hook" "$destfile" 2>/dev/null ||
        echo "refusing to overwrite pre-existing hook $hookname" >&2
done
