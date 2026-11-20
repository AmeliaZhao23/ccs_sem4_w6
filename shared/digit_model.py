"""Local handwritten-digit inference. Runtime dependencies: NumPy, Pillow."""
from pathlib import Path
from functools import lru_cache
import numpy as np
from PIL import Image


def prepare_image(image):
    """Return a normalized 28x28 L image (bright ink on black)."""
    if image is None:
        raise ValueError('Please draw a digit from 0 to 9 first!')
    pixels = np.asarray(image)
    if pixels.size == 0 or not np.isfinite(pixels).all():
        raise ValueError('Please draw a digit from 0 to 9 first!')
    if np.issubdtype(pixels.dtype, np.floating) and pixels.min() >= 0 and pixels.max() <= 1:
        pixels = pixels * 255
    source = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
    if source.mode == 'RGBA':
        background = Image.new('RGBA', source.size, 'white')
        source = Image.alpha_composite(background, source)
    gray = np.asarray(source.convert('L'), dtype=np.float32)
    if np.ptp(gray) < 8:
        raise ValueError('Please draw a digit from 0 to 9 first!')
    border = np.concatenate((gray[0], gray[-1], gray[:, 0], gray[:, -1]))
    if np.median(border) > 127:
        gray = 255 - gray
    gray = np.clip(gray - np.median(np.concatenate((gray[0], gray[-1], gray[:, 0], gray[:, -1]))), 0, 255)
    yy, xx = np.where(gray > max(16, float(gray.max()) * 0.12))
    if len(xx) < 3:
        raise ValueError('Please draw a digit from 0 to 9 first!')
    crop = Image.fromarray(gray[yy.min():yy.max()+1, xx.min():xx.max()+1].astype(np.uint8))
    scale = 20 / max(crop.size)
    size = tuple(max(1, round(dimension * scale)) for dimension in crop.size)
    crop = crop.resize(size, Image.Resampling.LANCZOS)
    canvas = Image.new('L', (28, 28), 0)
    canvas.paste(crop, ((28-size[0])//2, (28-size[1])//2))
    return canvas


@lru_cache(maxsize=1)
def _load_weights():
    with np.load(Path(__file__).resolve().with_name('model.npz'), allow_pickle=False) as archive:
        return tuple(archive[name].copy() for name in ('w1', 'b1', 'w2', 'b2'))


def predict(image) -> dict[str, float]:
    """Score a PIL image or NumPy uint8 array; keys are strings '0'..'9'.

    No network or training is used. Blank input raises a friendly ValueError.
    Softmax scores sum to one but are not calibrated certainty estimates.
    """
    prepared = prepare_image(image)
    x = np.asarray(prepared, dtype=np.float32).reshape(1, 784) / 255.0
    w1, b1, w2, b2 = _load_weights()
    logits = (np.maximum(x @ w1 + b1, 0) @ w2 + b2).reshape(10)
    probabilities = np.exp((logits - logits.max()).astype(np.float64))
    probabilities /= probabilities.sum()
    return {str(digit): float(probabilities[digit]) for digit in range(10)}
