#!/bin/bash
# Usage: ./render.sh E01 [E02 ...]   (full quality 1080p30, three scenes at a time)
#        QUALITY=l ./render.sh E01   (480p15 preview)
cd "$(dirname "$0")"
source ../../venv/bin/activate
Q=${QUALITY:-h}
if [ "$Q" = "l" ]; then QARGS="-ql"; else QARGS="-r 1920,1080 --fps 30"; fi
jobs=""
for ep in "$@"; do
  f=$(echo $ep | tr 'A-Z' 'a-z')
  for s in $(grep -o "^class ${ep}S[0-9][0-9]" scenes/$f.py | sed 's/class //'); do jobs="$jobs $f:$s"; done
done
echo $jobs | tr ' ' '\n' | xargs -P ${JOBS:-3} -I{} bash -c 'f=${1%%:*}; s=${1#*:}; manim '"$QARGS"' --disable_caching scenes/$f.py $s > media/log_$s.txt 2>&1 && echo "done $s" || echo "FAILED $s"' _ {}
