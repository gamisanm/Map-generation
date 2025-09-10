import noise
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

width, height = 300, 300
scale = 0.05
octaves = 6
persistence = 0.5
lacunarity = 2.0

textures = {
    "water": [np.array(Image.open("water.jpg"))],
    "sand": [np.array(Image.open("sand.jpg"))],
    "grass": [np.array(Image.open("grass.jpg"))],
            #   np.array(Image.open("grass2.jpg"))],
    "forest": [np.array(Image.open("forest.jpg"))],
            #    np.array(Image.open("forest2.jpg"))],/
    "mountain": [np.array(Image.open("mountain.jpg"))],
                #  np.array(Image.open("mountain2.jpg"))]
}

height_map = np.zeros((height, width))
for y in range(height):
    for x in range(width):
        height_map[y][x] = noise.pnoise2(
            x * scale,
            y * scale,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            repeatx=1024,
            repeaty=1024,
            base=42
        )

height_map = (height_map - height_map.min()) / (height_map.max() - height_map.min())

def get_biome(h):
    if h < 0.3:
        return "water"
    elif h < 0.4:
        return "sand"
    elif h < 0.6:
        return "grass"
    elif h < 0.8:
        return "forest"
    else:
        return "mountain"

def generate_map(height_map, textures, blend_radius=3):
    h, w = height_map.shape
    result = np.zeros((h, w, 3), dtype=np.uint8)

    rng = np.random.default_rng(seed=42)
    offset_map = rng.integers(0, 1000, size=(h, w))

    for y in range(h):
        for x in range(w):
            h_value = height_map[y, x]
            biome = get_biome(h_value)
            
            tex_list = textures[biome]
            tex = tex_list[offset_map[y, x] % len(tex_list)]
            tex_h, tex_w, _ = tex.shape

            pixel = tex[y % tex_h, x % tex_w].astype(float)

            blend_pixels = []
            blend_weights = []
            for dy in range(-blend_radius, blend_radius+1):
                for dx in range(-blend_radius, blend_radius+1):
                    ny = np.clip(y + dy, 0, h - 1)
                    nx = np.clip(x + dx, 0, w - 1)
                    neighbor_biome = get_biome(height_map[ny, nx])
                    if neighbor_biome != biome:
                        n_tex_list = textures[neighbor_biome]
                        n_tex = n_tex_list[offset_map[ny, nx] % len(n_tex_list)]
                        n_pixel = n_tex[ny % tex_h, nx % tex_w].astype(float)
                        weight = max(0, 1 - (abs(dx) + abs(dy)) / (blend_radius*2))
                        blend_pixels.append(n_pixel * weight)
                        blend_weights.append(weight)

            if blend_pixels:
                pixel = (pixel + sum(blend_pixels)) / (1 + sum(blend_weights))

            gx, gy = np.gradient(height_map)
            slope = np.sqrt(gx[y, x]**2 + gy[y, x]**2)
            shadow = np.clip(1 - slope * 2, 0.5, 1.0)  
            pixel *= shadow

            result[y, x] = np.clip(pixel, 0, 255)

    return result.astype(np.uint8)

final_map = generate_map(height_map, textures, blend_radius=4)

Image.fromarray(final_map).save("final/final_map.png")
plt.figure(figsize=(10,10))
plt.imshow(final_map)
plt.axis('off')
plt.show()
