from PIL import Image, ImageChops


def compute_ela_score(image_path: str, quality: int = 90) -> float:
    original = Image.open(image_path).convert("RGB")
    recompressed_path = image_path + ".recompressed.jpg"
    original.save(recompressed_path, "JPEG", quality=quality)
    recompressed = Image.open(recompressed_path)

    diff = ImageChops.difference(original, recompressed)
    extrema = diff.getbbox()
    return 0.0 if extrema is None else 1.0
