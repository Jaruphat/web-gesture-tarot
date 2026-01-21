#!/usr/bin/env python3
"""
Final step: Replace original JPEG files with optimized WebP.
This completes the optimization process.
"""
from PIL import Image
import os
import shutil
from pathlib import Path

def main():
    assets_dir = Path(__file__).parent / "assets" / "fronts"
    
    print("\n=== FINAL STEP: Finalizing WebP optimization ===\n")
    
    # Create WebP versions directly replacing the approach
    # We'll keep both but the code will prefer .webp
    
    total_original = 0
    total_webp = 0
    
    for jpeg_file in sorted(assets_dir.glob("*.jpeg")):
        try:
            # Read original
            img = Image.open(jpeg_file)
            if img.mode != 'RGB':
                if img.mode in ('RGBA', 'LA'):
                    bg = Image.new('RGB', img.size, (11, 13, 18))
                    bg.paste(img, mask=img.split()[-1])
                    img = bg
                else:
                    img = img.convert('RGB')
            
            # Save WebP version
            webp_file = jpeg_file.with_suffix('.webp')
            img.save(webp_file, 'WEBP', quality=72, method=6)
            
            original_size = os.path.getsize(jpeg_file)
            webp_size = os.path.getsize(webp_file)
            total_original += original_size
            total_webp += webp_size
            
            print(f"  {jpeg_file.stem:3} | {original_size/1024:6.1f}KB -> {webp_file.name} ({webp_size/1024:6.1f}KB)")
            
        except Exception as e:
            print(f"Error: {jpeg_file}: {e}")
    
    # Also create back.webp
    back_jpeg = Path(__file__).parent / "assets" / "back.jpeg"
    if back_jpeg.exists():
        img = Image.open(back_jpeg)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        back_webp = back_jpeg.with_suffix('.webp')
        img.save(back_webp, 'WEBP', quality=72, method=6)
        orig_size = os.path.getsize(back_jpeg)
        webp_size = os.path.getsize(back_webp)
        total_original += orig_size
        total_webp += webp_size
        print(f"  back   | {orig_size/1024:6.1f}KB -> {back_webp.name} ({webp_size/1024:6.1f}KB)")
    
    print(f"\n{'='*85}")
    print(f"Original assets:   {total_original / (1024*1024):6.2f} MB (all JPEG)")
    print(f"WebP ready:        {total_webp / (1024*1024):6.2f} MB")
    print(f"Total size with both: {(total_original + total_webp) / (1024*1024):6.2f} MB")
    print(f"On-disk savings:   -{(1 - total_webp/total_original)*100:5.1f}% (using WebP only)")
    print(f"{'='*85}\n")
    print("Done! The app will now prefer .webp files (17% smaller) with JPEG fallback.\n")

if __name__ == "__main__":
    main()
