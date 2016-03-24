#for f in database/*

for f in database/*

do
 #out=$(exiftool $f | grep GPS)
 out=$(exiftool $f | grep "GPS Position" | cut -d':' -f2)
 if  [[ $out ]]; then
    echo $f has GPS $out
    #echo $f has GPS >> log.txt
    #echo $f $out >> positionDB.txt
 else 
    rm $f
    echo $f removed
    echo $f removed >> log.txt
 fi
done
