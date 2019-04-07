

gunzip -c ed.gz | split -l 400000 -a 2 -d - ed.split.
gzip ed.split.*


