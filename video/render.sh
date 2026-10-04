#!/bin/bash
# Full-quality render of every scene (1080p30), three scenes at a time.
cd "$(dirname "$0")"
source ../venv/bin/activate
jobs=""
for f in partA:S01,S02,S03,S04,S05,S06,S07,S08 partB:S09,S10,S11,S12,S13,S14,S15,S16 partC:S17,S18,S19,S20,S21,S22,S23,S24 partD:S25,S26,S27,S28,S29,S30,S31; do
  file=${f%%:*}; scenes=${f#*:}
  for s in ${scenes//,/ }; do jobs="$jobs $file:$s"; done
done
echo $jobs | tr ' ' '\n' | xargs -P 3 -I{} bash -c 'f=${1%%:*}; s=${1#*:}; manim -r 1920,1080 --fps 30 --disable_caching scenes/$f.py $s > media/log_$s.txt 2>&1 && echo "done $s" || echo "FAILED $s"' _ {}
