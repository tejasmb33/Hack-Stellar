#!/bin/sh
set -eu

rm -rf dist
mkdir -p dist

cp index.html credits.html styles.css app.js gallery.js scene.js dist/
cp -R assets vendor visuals problem-statements dist/