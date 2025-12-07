SEED=42
SUBJECTS=(duck_toy dog6 robot_toy backpack_dog vase poop_emoji bear_plushie clock)

for ((i=0; i<${#SUBJECTS[@]}; i++)); do
    for ((j=i+1; j<${#SUBJECTS[@]}; j++)); do
        for LAMBDA in 0.0 0.01 0.1 1.0; do
            SUBJECT1=${SUBJECTS[i]}
            SUBJECT2=${SUBJECTS[j]}
            
            OUTPUT_DIR="outputs"
            PROMPT="$SUBJECT1, $SUBJECT2"
            ZIPLORA_NAME="$SUBJECT1-$SUBJECT2-lambda-$LAMBDA"

            echo "Generating $ZIPLORA_NAME..."

            python generate.py \
            --ziplora_name $ZIPLORA_NAME \
            --prompt "$PROMPT"\
            --output_dir $OUTPUT_DIR \
            --seed $SEED
        done
    done
done