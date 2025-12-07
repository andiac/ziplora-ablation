SUBJECTS=$(basename -a single-lora/*/)

echo "Removing temporary checkpoints for the following subjects: $SUBJECTS"

for SUBJECT in $SUBJECTS; do
    rm -rf "single-lora/$SUBJECT/checkpoint-500"
    rm -rf "single-lora/$SUBJECT/checkpoint-1000"
    echo "Removed temporary checkpoints for $SUBJECT"
done
