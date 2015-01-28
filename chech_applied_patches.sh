#!/bin/bash
for p in `find . -name '*.patch'`; do
    SHA=$(grep '^From ' $p | cut -d ' ' -f 2);
    V=$(git tag --contains $SHA | grep $1);
    if [ "$V" == "" ]; then
        echo "** $p not in version $1";
    fi;
done