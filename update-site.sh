#!/bin/sh
# Copies un-final-idea/site into the public heat-shutoff-check repo and pushes it.
set -e
D=$(mktemp -d)
gh repo clone TommyWang469/heat-shutoff-check "$D/pub" -- -q
cd "$D/pub"
cp "$HOME/Documents/GitHub/un-final-idea/site/"* .
git add .
git commit -q -m "${1:-Update site}"
git push -q origin main
echo "Pushed. Live in about a minute."
