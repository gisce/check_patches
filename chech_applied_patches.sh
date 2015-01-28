#!/bin/bash
V=$(git tag | grep $1)
if [ "x$V" = "x" ]; then
    echo "**** This repo is not upgraded to version $V";
fi
for p in `find . -name '*.patch'`; do
    SHA=$(grep '^From ' $p | cut -d ' ' -f 2);
    V=$(git tag --contains $SHA | grep $1);
    if [ "x$V" == "x" ]; then
        echo "**** ($SHA) $p not in version $1";
    fi;
done