"""PASS B — PIL storybook grade for the Kuwahara look-dev (runs on SYSTEM python; Blender's bundled
python has no PIL). Takes the Blender pre-PIL render (already Kuwahara-smoothed) and adds the final
matte-storybook 'paint' feel: gentle edge-preserving smooth + warm saturation + soft bloom.

  python3 lookdev_kuwahara_post.py <prePIL.png> <final.png>
"""
import sys
from PIL import Image, ImageFilter, ImageEnhance, ImageChops

pre, out = sys.argv[1], sys.argv[2]
im = Image.open(pre).convert("RGB")

# 1) light median to fuse any remaining micro-fur into painterly patches (gentle; eyes/edges survive)
paint = im.filter(ImageFilter.MedianFilter(size=3))
# 2) a subtle SMOOTH to melt plasticky specular micro-detail into matte
paint = paint.filter(ImageFilter.SMOOTH)
# keep some original edge crispness (eyes/collar/tag) by blending back toward the source
paint = Image.blend(im, paint, 0.65)

# 3) slight warm saturation + tiny contrast lift for the storybook pop
paint = ImageEnhance.Color(paint).enhance(1.13)
paint = ImageEnhance.Contrast(paint).enhance(1.05)

# 4) soft bloom: blur a dimmed copy and screen it back lightly for matte warmth
blur = paint.filter(ImageFilter.GaussianBlur(6))
dim = blur.point(lambda p: int(p * 0.18))
bloom = ImageChops.screen(paint, dim)
paint = Image.blend(paint, bloom, 0.32)

paint.save(out)
print("PIL storybook grade DONE ->", out)
