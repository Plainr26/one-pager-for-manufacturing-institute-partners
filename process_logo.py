import os
from PIL import Image

def process_logo():
    src_path = r"C:\Users\LydiaHunterLabsTech\.gemini\antigravity\brain\9def097c-a583-4bdb-a158-75b6dadf89e3\media__1779840964441.png"
    dest_dir = r"C:\Users\LydiaHunterLabsTech\.gemini\antigravity\scratch\Plainr-Manufacturing-OnePager"
    
    if not os.path.exists(src_path):
        print(f"Error: source file not found at {src_path}")
        return

    # Open image and convert to RGBA
    img = Image.open(src_path).convert('RGBA')
    width, height = img.size
    print(f"Image loaded. Size: {width}x{height}")

    # Create new images for output
    img_icon_only = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    img_full_white = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    # List to track bounding box of the purple icon
    purple_xs = []
    purple_ys = []

    # Process pixels
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            
            # Black background is around (0,0,0)
            if r < 10 and g < 15 and b < 10:
                continue
            
            # Check if purple (icon)
            # Purple has high R and B relative to G
            is_purple = (r > 20 and b > 20 and g < r * 0.8 and g < b * 0.8)
            
            if is_purple:
                purple_xs.append(x)
                purple_ys.append(y)
                
                # Robust threshold-based alpha scaling for the icon
                # Original purple intensity max is ~139, so let's set threshold to 80
                # Any intensity >= 80 becomes fully opaque (alpha 255)
                # Intensities below 80 are scaled linearly to preserve beautiful anti-aliased edge smoothing
                orig_val = max(r, b)
                if orig_val >= 80:
                    alpha = 255
                else:
                    alpha = int(orig_val * (255.0 / 80.0))
                
                # White pixel for icon
                img_icon_only.putpixel((x, y), (255, 255, 255, alpha))
                img_full_white.putpixel((x, y), (255, 255, 255, alpha))
                
            elif r > 12 or g > 12 or b > 12:
                # This is the grey text "plainr"
                # Since grey text is dark (intensity around 30-50), we use a threshold of 35
                # Any grey intensity >= 35 becomes solid white (alpha 255)
                # Intensities below 35 are scaled linearly to preserve perfect text antialiasing
                orig_val = max(r, g, b)
                if orig_val >= 35:
                    alpha = 255
                else:
                    alpha = int(orig_val * (255.0 / 35.0))
                
                # Full white image gets the crisp white text
                img_full_white.putpixel((x, y), (255, 255, 255, alpha))

    # Save full logo (white on transparent)
    full_white_path = os.path.join(dest_dir, "logo_full.png")
    img_full_white.save(full_white_path, "PNG")
    print(f"Saved full solid white logo to: {full_white_path}")

    # Crop the icon only
    if purple_xs and purple_ys:
        min_x, max_x = min(purple_xs), max(purple_xs)
        min_y, max_y = min(purple_ys), max(purple_ys)
        
        # Add some padding
        padding = 4
        crop_box = (
            max(0, min_x - padding),
            max(0, min_y - padding),
            min(width, max_x + padding + 1),
            min(height, max_y + padding + 1)
        )
        
        cropped_icon = img_icon_only.crop(crop_box)
        icon_path = os.path.join(dest_dir, "logo_icon.png")
        cropped_icon.save(icon_path, "PNG")
        print(f"Saved cropped icon to: {icon_path} (box: {crop_box})")
    else:
        print("Could not crop icon: no purple pixels found in scan.")

if __name__ == "__main__":
    process_logo()
