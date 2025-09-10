# 🗺️ 2D Procedural Map Generator with Perlin Noise and Textures

**This project generates realistic 2D maps using Perlin noise, with textures, smooth biome transitions, shadows, and random variations for natural-looking terrain.**  

---

## **Features**

- 🌊 **Water, Sand, Grass, Forest, Mountain** biomes  
- 🎨 **Custom textures** for each biome (support for multiple variants)  
- 🌄 **Shading based on terrain slope** for a pseudo-3D effect  
- 🔄 **Smooth transitions** between biomes  
- 🎲 **Random texture variation** to avoid repetition  
- 🖼️ Generates high-resolution maps ready for games or creative projects  

---

## **How It Works**

1. Generate a **height map** using Perlin noise.  
2. Assign each pixel a **biome** based on height thresholds.  
3. Apply **corresponding texture** for each biome.  
4. Smooth edges by **blending neighboring biomes**.  
5. Add **shadows** based on terrain gradient.  
6. Introduce **random texture variations** for more natural look.  

---

## **Usage**
# Clone this repository
git clone https://github.com/yourusername/procedural-map-generator.git
cd procedural-map-generator

# Install dependencies
pip install numpy pillow matplotlib noise

# Run the generator
python generate_map.py
