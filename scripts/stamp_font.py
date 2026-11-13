import random
import numpy as np

from pathlib import Path
from PIL import Image


def load_glyphs():
    asset_folder = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "stamp_glyphs"
    )

    base_folder = asset_folder / "base"
    variants_folder = asset_folder / "variants"

    characters = "0123456789A-"
    glyphs = {}

    for char in characters:
        filename = "hyphen.png" if char == "-" else f"{char}.png"

        base_path = base_folder / filename

        if not base_path.exists():
            raise FileNotFoundError(
                f"Missing base glyph: {base_path}"
            )

        glyphs[char] = [
            Image.open(base_path).convert("RGBA")
        ]

        # Load additional variants, except for the hyphen
        if char != "-":
            char_folder = variants_folder / char

            if char_folder.exists():
                for path in sorted(char_folder.glob("*.png")):
                    glyphs[char].append(
                        Image.open(path).convert("RGBA")
                    )

    return glyphs


def render_text(text, glyphs, height=48, spacing=3, seed=None):
    rng = random.Random(seed)

    missing = set(text) - set(glyphs)

    if missing:
        raise ValueError(f"Unsupported characters: {missing}")

    resized_glyphs = []
    previous_char = None
    previous_index = None

    for char in text:
        variants = glyphs[char]

        # Avoid repeating the same glyph for consecutive identical characters
        if char == previous_char and len(variants) > 1:
            choices = [
                i for i in range(len(variants))
                if i != previous_index
            ]
            variant_index = rng.choice(choices)
        else:
            variant_index = rng.randrange(len(variants))

        glyph = variants[variant_index]
        # Remove transparent padding around the glyph
        bbox = glyph.getchannel("A").getbbox()

        if bbox:
            glyph = glyph.crop(bbox)

        previous_char = char
        previous_index = variant_index

        target_height = round(height * 0.22) if char == "-" else height

        scale = target_height / glyph.height
        new_width = max(1, round(glyph.width * scale))

        resized = glyph.resize(
            (new_width, target_height),
            Image.Resampling.LANCZOS
        )

        resized_glyphs.append((char, resized))

    total_width = (
        sum(glyph.width for _, glyph in resized_glyphs)
        + spacing * (len(resized_glyphs) - 1)
    )

    result = Image.new("RGBA", (total_width, height), (0, 0, 0, 0))

    x = 0

    for char, glyph in resized_glyphs:
        y = (height - glyph.height) // 2 if char == "-" else 0
        result.alpha_composite(glyph, (x, y))
        x += glyph.width + spacing

    return result


def apply_ink_texture(image, seed=None):
    rng = np.random.default_rng(seed)

    pixels = np.array(image).copy()
    alpha = pixels[:, :, 3].astype(np.float32)

    height, width = alpha.shape

    # Create subtle opacity variations across the ink
    noise = rng.normal(
        loc=0.96,
        scale=0.06,
        size=(height, width)
    )

    noise = np.clip(noise, 0.72, 1.0)

    # Apply variations only where ink exists
    textured_alpha = alpha * noise

    # Add a few tiny, localized ink gaps
    gaps = rng.random((height, width)) < 0.0015
    textured_alpha[gaps] = 0

    pixels[:, :, 3] = np.clip(
        textured_alpha, 0, 255
    ).astype(np.uint8)

    return Image.fromarray(pixels, "RGBA")

def generate_stamp(text, output_path, seed=None):
    glyphs = load_glyphs()

    image = render_text(text, glyphs, seed=seed)

    #image = apply_ink_texture(image, seed)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image.save(output_path)

    return output_path
