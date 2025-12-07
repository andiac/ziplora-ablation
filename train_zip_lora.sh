MODEL_NAME="stabilityai/stable-diffusion-xl-base-1.0"

SUBJECTS=(duck_toy robot_toy backpack_dog poop_emoji bear_plushie clock)

for ((i=0; i<${#SUBJECTS[@]}; i++)); do
    for ((j=i+1; j<${#SUBJECTS[@]}; j++)); do
        for LAMBDA in 0.0 0.01 0.1 1.0; do
            SUBJECT1=${SUBJECTS[i]}
            SUBJECT2=${SUBJECTS[j]}
            
            mkdir -p "ziplora/$SUBJECT1-$SUBJECT2-lambda-$LAMBDA"
            OUTPUT_DIR="ziplora/$SUBJECT1-$SUBJECT2-lambda-$LAMBDA"
            
            LORA_PATH1="single-lora/$SUBJECT1"
            INSTANCE_DIR1="../dreambooth/dataset/$SUBJECT1"
            PROMPT1="a $SUBJECT1"

            LORA_PATH2="single-lora/$SUBJECT2"
            INSTANCE_DIR2="../dreambooth/dataset/$SUBJECT2"
            PROMPT2="a $SUBJECT2"

            VALID_PROMPT="$SUBJECT1, $SUBJECT2"

            accelerate launch train_dreambooth_ziplora_sdxl.py \
            --pretrained_model_name_or_path=$MODEL_NAME \
            --output_dir=$OUTPUT_DIR \
            --lora_name_or_path=$LORA_PATH1 \
            --instance_prompt="${PROMPT1}" \
            --instance_data_dir=$INSTANCE_DIR1 \
            --lora_name_or_path_2=$LORA_PATH2 \
            --instance_prompt_2="${PROMPT2}" \
            --instance_data_dir_2=$INSTANCE_DIR2 \
            --resolution=1024 \
            --train_batch_size=1 \
            --learning_rate=5e-5 \
            --similarity_lambda=$LAMBDA \
            --lr_scheduler="constant" \
            --lr_warmup_steps=0 \
            --max_train_steps=100 \
            --validation_prompt="${VALID_PROMPT}" \
            --validation_epochs=10 \
            --seed="0" \
            --mixed_precision="fp16" \
            --gradient_checkpointing \
            --use_8bit_adam
        done
    done
done
