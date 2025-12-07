from PIL import Image

subjects = ["duck_toy", "robot_toy", "backpack_dog", "poop_emoji", "bear_plushie", "clock"]
subject_pairs = [("duck_toy", "backpack_dog"),
                 ("robot_toy", "poop_emoji"),
                 ("robot_toy", "bear_plushie"),
                 ("backpack_dog", "poop_emoji"),
                 ("poop_emoji", "bear_plushie")]
lambdas = [0.0, 0.01, 0.1, 1.0]

def show_images(images, suffix=""):
    img_size = 256
    images = [image.resize((img_size, img_size)) for image in images]

    # create a new image with 6 columns and 3 rows
    new_image = Image.new("RGB", (img_size * 6, img_size * 3))
    for i in range(len(images)):
        new_image.paste(images[i], (i % 6 * img_size, i // 6 * img_size))

    new_image.save(f"showcase{suffix}.png")

    import matplotlib.pyplot as plt
    import io

    header_height = 90
    labels = ["LoRA1", "LoRA2", r"$\lambda=0.0$", r"$\lambda=0.01$", r"$\lambda=0.1$", r"$\lambda=1.0$"]

    def render_latex_label(text, fontsize=20):
        fig, ax = plt.subplots(figsize=(2, 0.8), dpi=100)
        ax.text(0.5, 0.5, text, fontsize=fontsize, ha='center', va='center')
        ax.axis('off')
        fig.patch.set_facecolor('white')
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, facecolor='white')
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)

    final_image = Image.new("RGB", (img_size * 6, img_size * 3 + header_height), "white")
    final_image.paste(new_image, (0, header_height))

    for i, label in enumerate(labels):
        label_img = render_latex_label(label)
        x = i * img_size + img_size // 2 - label_img.width // 2
        y = header_height // 2 - label_img.height // 2
        final_image.paste(label_img, (x, y))

    final_image.save(f"showcase-with-text{suffix}.png")

images = []

for subject1, subject2 in subject_pairs:
    images.append(Image.open(f"single-lora/{subject1}/test_images/final_image_00.png"))
    images.append(Image.open(f"single-lora/{subject2}/test_images/final_image_00.png"))

    for lambda_ in lambdas:
        image = Image.open(f"outputs/{subject1}-{subject2}-lambda-{lambda_}.png")
        images.append(image)

show_images(images)

images = []

for i in range(len(subjects)):
    for j in range(i+1, len(subjects)):
        subject1 = subjects[i]
        subject2 = subjects[j]

    images.append(Image.open(f"single-lora/{subject1}/test_images/final_image_00.png"))
    images.append(Image.open(f"single-lora/{subject2}/test_images/final_image_00.png"))

    for lambda_ in lambdas:
        image = Image.open(f"outputs/{subject1}-{subject2}-lambda-{lambda_}.png")
        images.append(image)

show_images(images, suffix="-all")
