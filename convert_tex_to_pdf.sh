#!/bin/zsh
find static/uploads/problem -name '*.tex' | while read texfile; do
    pdfdir=$(dirname "$texfile")
    cd "$pdfdir"
    latexmk -pdf -silent "$(basename "$texfile")"
    cd -
done
