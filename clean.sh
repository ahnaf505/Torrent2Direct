#!/bin/bash

if [ ! -d "bin" ]; then
  mkdir bin
fi

if [ "$(ls -A bin)" ]; then
  if [ ! -d "archive" ]; then
    mkdir archive
  fi
  mv bin/* archive/
fi

if [ -f "dist/main.bin" ]; then
  mv dist/main.bin bin/
fi

if [ "$(ls -A bin)" ]; then
  for file in bin/*; do
    hash=$(sha256sum "$file" | awk '{print $1}')
    timestamp=$(date +"%Y%m%d%H%M%S")
    random_number=$((RANDOM))
    extension="${file##*.}"
    
    mv "$file" "bin/Torrent2Direct${hash}_${timestamp}_${random_number}.${extension}"
  done
fi

if [ -d "dist" ]; then
  rm -rf dist
fi

