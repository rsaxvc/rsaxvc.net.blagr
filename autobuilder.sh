#!/bin/bash

while true; do
	change=$(inotifywait -r -e close_write,moved_to,create input)
	./build_blog.sh
	#sensible-browser ../blog/index.html
done
