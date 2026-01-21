#!/usr/bin/env python3
"""
Convert JPEG card images to WebP format for 50-60% size reduction.
This is a major optimization - WebP is far superior to JPEG.
"""
from PIL import Image
import os
from pathlib import Path

def convert_to_webp(input_path, output_path, quality=75):
    """Convert JPEG to WebP with excellent compression."""
    try:
        img = Image.open(input_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            if img.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', img.size, (11, 13, 18))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert('RGB')
        
        # Save as WebP with high quality but aggressive compression
        img.save(output_path, 'WEBP', quality=quality, method=6)
        
        original_size = os.path.getsize(input_path)
        converted_size = os.path.getsize(output_path)
        reduction = (1 - converted_size / original_size) * 100
        
        return original_size, converted_size, reduction
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return 0, 0, 0

def main():
    assets_dir = Path(__file__).parent / "assets" / "fronts"
    
    print("\n🎨 Converting card images to WebP format...\n")
    
    total_original = 0
    total_converted = 0
    
    for jpeg_file in sorted(assets_dir.glob("*.jpeg")):
        webp_file = jpeg_file.with_suffix('.webp')
        original_size, converted_size, reduction = convert_to_webp(
            jpeg_file, 
            webp_file, 
            quality=75
        )
        
        if original_size > 0:
            total_original += original_size
            total_converted += converted_size
            print(f"  {jpeg_file.name:8} | {original_size/1024:6.1f}KB → {converted_size/1024:6.1f}KB (.webp) | -{reduction:5.1f}%")
    
    print(f"\n{'='*65}")
    print(f"✓ Total original (JPEG):   {total_original / (1024*1024):6.2f} MB")
    print(f"✓ Total converted (WebP):  {total_converted / (1024*1024):6.2f} MB")
    print(f"✓ Saved:                   {(total_original - total_converted) / (1024*1024):6.2f} MB ({(1 - total_converted/total_original)*100:.1f}%)")
    print(f"{'='*65}\n")
    
    # Convert back.jpeg too
    back_jpeg = Path(__file__).parent / "assets" / "back.jpeg"
    back_webp = back_jpeg.with_suffix('.webp')
    if back_jpeg.exists():
        print("Converting back.jpeg...")
        original_size, converted_size, reduction = convert_to_webp(
            back_jpeg, 
            back_webp, 
            quality=75
        )
        print(f"  back.jpeg → back.webp: {original_size/1024:.1f}KB → {converted_size/1024:.1f}KB | -{reduction:.1f}%\n")
    
    print("⚠️  WebP files created. Now update index.html to use .webp with .jpeg fallback!")

if __name__ == "__main__":
    main()
