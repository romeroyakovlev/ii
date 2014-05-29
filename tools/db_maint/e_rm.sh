#!/bin/sh

for e in $@
do
for n in `cat echo/$e`
do
rm msg/$n
done
rm echo/$e
done
