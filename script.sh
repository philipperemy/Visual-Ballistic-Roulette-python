#!/usr/bin/env bash
for file in **/*.py; rm $file
for file in **/*.java; j2py $file > "${file%.java}".py;
for file in **/*.py; gsed -r "s/([a-z]+)([A-Z][a-z]+)/\1_\l\2/g" $file > $file.new;
for file in **/*.py; rm $file;
for file in **/*.py.new; mv $file ${file%.new};
