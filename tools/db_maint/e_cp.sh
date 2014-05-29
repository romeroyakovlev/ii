#!/bin/sh

mkdir -p cp/msg
mkdir -p cp/echo

for e in $@
do
cp echo/$e cp/echo/$e
for n in `cat echo/$e`
do
cp msg/$n cp/msg/$n
done
done