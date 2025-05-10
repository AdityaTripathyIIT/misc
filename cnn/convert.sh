#!/bin/bash

INPUT_DIR="test"
OUTPUT_DIR="test"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*; do
    if magick identify "$file" &>/dev/null; then
        filename=$(basename "$file")
        name="${filename%.*}"
        magick "$file" "$OUTPUT_DIR/$name.jpg"
        echo "Converted: $filename -> $name.jpg"
    else
        echo "Skipped (not an image or unsupported): $file"
    fi
done

