# clear positionDB
echo "" > positionDB.txt 

# loop trough the database
for f in database/*
do
 # get EXIF GPS data
 out=$(exiftool $f | grep "GPS Position" | cut -d':' -f2)
 
 # if it has a GPS position
 if  [[ $out ]]; then
    # commented out
    #echo $f $out >> positionDB.txt
    
    # print the converted value
    pos=$(python convDBLine.py "$f$out")
    echo $pos
    echo $pos >> positionDB.txt
    
    # and rdo the conversion for the logs
    #python convDBLine.py "$f$out" >> positionDB.txt
    
 else 
    rm $f
    echo $f removed
    echo $f removed >> log.txt
 fi
done
