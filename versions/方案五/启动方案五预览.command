#!/bin/zsh
cd "$(dirname "$0")" || exit 1
if python3 -c 'import json,pathlib,urllib.request; d=json.load(urllib.request.urlopen("http://127.0.0.1:3005/scope.json",timeout=1)); assert pathlib.Path(d["output_root"]) == pathlib.Path.cwd()' 2>/dev/null; then
  open 'http://127.0.0.1:3005/'
  exit 0
fi
python3 scripts/serve.py --port 3005 &
preview_pid=$!
trap 'kill "$preview_pid" 2>/dev/null' EXIT INT TERM
python3 -c 'import time,urllib.request
for attempt in range(30):
 try:
  urllib.request.urlopen("http://127.0.0.1:3005/",timeout=1).close();break
 except Exception: time.sleep(.1)'
open 'http://127.0.0.1:3005/'
wait "$preview_pid"
