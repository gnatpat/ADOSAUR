

if [ $# = 0 ]; then
    echo "Usage: $0 input [output saveLog]"
    echo "Defaults:"
    echo "\tOutput: output.arff"
    echo "\tsaveLog: N"
    exit 1
fi

INPUT=$1
if [ $# = 1 ]; then
    OUTPUT="output.arff"
else
    OUTPUT=$2
fi
if [ $# -le 2 ]; then
    SAVELOG="N"
else
    SAVELOG=$3
fi

echo "Extracting features from $INPUT..."
SMILExtract -C config/avec2013.conf -I $INPUT
mv output.arff $OUTPUT 
echo "Done. Saved to $OUTPUT"

if [ "$SAVELOG" = "N" ]; then
    rm -f smile.log
    echo "Cleaned up smile.log"
fi

