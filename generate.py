import os
import argparse
import torch
from diffusers import StableDiffusionXLPipeline
from ziplora_pytorch.utils import insert_ziplora_to_unet

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ziplora_name", type=str, required=True, help="ziplora")
    parser.add_argument("--prompt", type=str, required=True, help="prompt")
    parser.add_argument("--output_dir", type=str, default="outputs", help="output directory")
    parser.add_argument("--seed", type=int, default=42, help="seed")
    return parser.parse_args()

args = parse_args()

os.makedirs(args.output_dir, exist_ok=True)

pipeline = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0"
)

pipeline.unet = insert_ziplora_to_unet(
    pipeline.unet, 
    f"ziplora/{args.ziplora_name}"
)
pipeline.to(device="cuda", dtype=torch.float16)

image = pipeline(prompt=args.prompt, generator=torch.Generator(device="cuda").manual_seed(args.seed)).images[0]
image.save(os.path.join(args.output_dir, f"{args.ziplora_name}.png"))
