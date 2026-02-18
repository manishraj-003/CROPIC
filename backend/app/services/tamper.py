from PIL import Image, ImageChops, ImageEnhance


def ela_score(image_path: str, quality: int = 90) -> float:
    original = Image.open(image_path).convert("RGB")
    temp_path = image_path + ".ela_temp.jpg"
    original.save(temp_path, "JPEG", quality=quality)

    recompressed = Image.open(temp_path)
    diff = ImageChops.difference(original, recompressed)
    extrema = diff.getextrema()

    max_diff = max(channel_max for _, channel_max in extrema)
    scale = 255.0 / max_diff if max_diff else 1.0
    enhanced = ImageEnhance.Brightness(diff).enhance(scale)

    histogram = enhanced.histogram()
    total = sum(i * v for i, v in enumerate(histogram))
    pixels = sum(histogram)
    return total / pixels if pixels else 0.0
