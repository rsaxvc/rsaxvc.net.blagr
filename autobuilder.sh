#!/bin/bash

command -v inotifywait >/dev/null 2>&1 || { echo >&2 "I require inotifywait but it's not installed.  Aborting."; exit 1; }

while true; do
	change=$(inotifywait -r -e close_write,moved_to,create input)
	./build_blog.sh
	#sensible-browser ../blog/index.html
done
