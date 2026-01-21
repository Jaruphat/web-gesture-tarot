#!/usr/bin/env python3
"""
Compress card images aggressively while maintaining visual quality.
Target: 14.18 MB -> ~4-5 MB (65% reduction)
"""
from PIL import Image
import os
from pathlib import Path

def compress_image(input_path, output_path, quality=65, max_width=800):
    """Compress JPEG image with size optimization."""
    try:
        img = Image.open(input_path)
        original_format = img.format
        
        # Always resize to max_width for consistency
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if needed (remove alpha)
        if img.mode != 'RGB':
            if img.mode in ('RGBA', 'LA'):
                bg = Image.new('RGB', img.size, (11, 13, 18))
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert('RGB')
        
        # Save with aggressive compression - force re-encoding
        img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=False)
        
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size / original_size) * 100
        
        return original_size, compressed_size, reduction
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return 0, 0, 0

def main():
    assets_dir = Path(__file__).parent / "assets" / "fronts"
    backup_dir = Path(__file__).parent / "assets" / "fronts_backup"
    
    # Create backup
    if not backup_dir.exists():
        backup_dir.mkdir(parents=True)
        for jpeg_file in sorted(assets_dir.glob("*.jpeg")):
            import shutil
            shutil.copy2(jpeg_file, backup_dir / jpeg_file.name)
        print(f"✓ Backup created in {backup_dir}")
    
    print("\n🎨 Compressing card images...\n")
    
    total_original = 0
    total_compressed = 0
    total_saved = 0
    
    for jpeg_file in sorted(assets_dir.glob("*.jpeg")):
        original_size, compressed_size, reduction = compress_image(
            jpeg_file, 
            jpeg_file, 
            quality=65,  # aggressive compression
            max_width=800  # resize to 800px max width
        )
        
        if original_size > 0:
            total_original += original_size
            total_compressed += compressed_size
            total_saved += original_size - compressed_size
            
            print(f"  {jpeg_file.name:8} | {original_size/1024:6.1f}KB → {compressed_size/1024:6.1f}KB | -{reduction:5.1f}%")
    
    print(f"\n{'='*60}")
    print(f"✓ Total original:   {total_original / (1024*1024):6.2f} MB")
    print(f"✓ Total compressed: {total_compressed / (1024*1024):6.2f} MB")
    print(f"✓ Saved:            {total_saved / (1024*1024):6.2f} MB ({(1 - total_compressed/total_original)*100:.1f}%)")
    print(f"{'='*60}\n")
    
    # Compress back.jpeg too
    back_file = Path(__file__).parent / "assets" / "back.jpeg"
    if back_file.exists():
        print("Compressing back.jpeg...")
        original_size, compressed_size, reduction = compress_image(
            back_file, 
            back_file, 
            quality=65,
            max_width=800
        )
        print(f"  back.jpeg: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB | -{reduction:.1f}%\n")

if __name__ == "__main__":
    main()
