#!/usr/bin/env python3
"""
Aggressive optimization: 
1. Create lower quality JPEG as fallback (quality 60)
2. Create super aggressive WebP (quality 60)
3. This should achieve 40-50% total size reduction
"""
from PIL import Image
import os
from pathlib import Path

def save_image(img, output_path, format_type, quality):
    """Save image in specified format."""
    try:
        if img.mode != 'RGB':
            if img.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', img.size, (11, 13, 18))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert('RGB')
        
        if format_type == 'JPEG':
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
        else:  # WebP
            img.save(output_path, 'WEBP', quality=quality, method=6)
        
        return os.path.getsize(output_path)
    except Exception as e:
        print(f"Error saving {output_path}: {e}")
        return 0

def main():
    assets_dir = Path(__file__).parent / "assets" / "fronts"
    
    print("\n=== AGGRESSIVE OPTIMIZATION: Creating both WebP (q60) and JPEG (q60) ===\n")
    
    total_original = 0
    total_webp_size = 0
    total_jpeg_size = 0
    
    for jpeg_file in sorted(assets_dir.glob("*.jpeg")):
        try:
            img = Image.open(jpeg_file)
            original_size = os.path.getsize(jpeg_file)
            total_original += original_size
            
            webp_file = jpeg_file.with_stem(jpeg_file.stem + "_opt").with_suffix('.webp')
            webp_size = save_image(img, webp_file, 'WEBP', quality=60)
            total_webp_size += webp_size
            
            # Create optimized JPEG for fallback
            jpeg_opt_file = jpeg_file.with_stem(jpeg_file.stem + "_opt").with_suffix('.jpeg')
            jpeg_size = save_image(img, jpeg_opt_file, 'JPEG', quality=60)
            total_jpeg_size += jpeg_size
            
            # Use smaller one
            best_size = min(webp_size, jpeg_size)
            best_format = 'WebP' if webp_size < jpeg_size else 'JPEG'
            
            print(f"  {jpeg_file.stem:3} | {original_size/1024:6.1f}KB -> WebP:{webp_size/1024:5.1f}KB  JPEG:{jpeg_size/1024:5.1f}KB  Best:{best_format} ({best_size/1024:5.1f}KB) -{(1-best_size/original_size)*100:5.1f}%")
            
        except Exception as e:
            print(f"Error processing {jpeg_file}: {e}")
    
    print(f"\n{'='*85}")
    print(f"OK Original JPEG total:  {total_original / (1024*1024):6.2f} MB")
    print(f"OK WebP (q60) total:     {total_webp_size / (1024*1024):6.2f} MB ({(1-total_webp_size/total_original)*100:5.1f}% reduction)")
    print(f"OK JPEG (q60) total:     {total_jpeg_size / (1024*1024):6.2f} MB ({(1-total_jpeg_size/total_original)*100:5.1f}% reduction)")
    print(f"{'='*85}\n")

if __name__ == "__main__":
    main()
