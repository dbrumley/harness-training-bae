#!/bin/sh

dot -Tpng graphs/graph-0.dot -o graphs/graph-0.png
dot -Tpng graphs/graph-1.dot -o graphs/graph-1.png
dot -Tpng graphs/graph-2.dot -o graphs/graph-2.png
dot -Tpng graphs/graph-3.dot -o graphs/graph-3.png
dot -Tpng graphs/graph-4.dot -o graphs/graph-4.png

pandoc \
    methodology-part-one.md \
    --toc \
    -H template-header.html \
    -B template-before-body.html \
    -A template-after-body.html \
> methodology-part-one.html

pandoc \
    methodology-part-one.md \
    --toc \
    -H template-header.tex \
    -o methodology-part-one.pdf