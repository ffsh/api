#!/bin/bash
url="https://map.freifunk-suedholstein.de/data/meshviewer.json"

FILES=("/home/grotax/git/api/badoldesloe.json" "/home/grotax/git/api/lauenburg.json" "/home/grotax/git/api/ratzeburg.json" "/home/grotax/git/api/reinbek.json" "/home/grotax/git/api/suedholstein.json")
echo $url
for FILE in ${FILES[*]}
do
    apiupdater -filename $FILE -url $url
done
