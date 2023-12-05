from PIL import Image, ImageOps
img = Image.open("output/cihp_parsing_maps/00891_00_vis.png")
img = ImageOps.exif_transpose(img)

img = img.resize((768, 1024), Image.NEAREST)
img = img.convert("P")

img.save("00891_00_upsampled.png", format="png")