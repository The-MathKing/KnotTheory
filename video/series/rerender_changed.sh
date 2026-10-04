#!/bin/bash
# Re-render the scenes listed in changed_scenes.txt at full quality, then re-assemble every episode.
cd "$(dirname "$0")"
source ../../venv/bin/activate
for s in $(cat changed_scenes.txt); do f=$(echo ${s:0:3} | tr 'A-Z' 'a-z'); echo "scenes/$f.py:$s"; done | xargs -P 3 -I{} bash -c 'f=${1%%:*}; s=${1#*:}; manim -r 1920,1080 --fps 30 --disable_caching $f $s > media/log_$s.txt 2>&1 && echo "done $s" || echo "FAILED $s"' _ {}
python3 assemble.py E01 E02 E03 E04 E05 E06 E07 E08 E09 E10 E11 E12 E13 E14 E15
