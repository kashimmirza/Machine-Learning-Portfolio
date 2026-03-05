import os
import re

src_dir = r"d:\Machine-Learning-Portfolio\AI_medical_projects\HEALTHWISE-HACKKU25\frontend\src"

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count how deep this file is from src/
        rel = os.path.relpath(filepath, src_dir)
        depth = len(os.path.dirname(rel).split(os.sep))
        prefix = "../" * depth
        
        original = content
        
        # Replace all component/lib imports
        content = re.sub(r'from\s+["\']\.\.\/\.\.\/components', f'from "{prefix}components', content)
        content = re.sub(r'from\s+["\']\.\.\/\.\.\/libs', f'from "{prefix}libs', content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {rel} → {prefix}")
            return True
    except Exception as e:
        print(f"✗ Error: {filepath} - {e}")
    return False

# Fix all TypeScript files
count = 0
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.tsx', '.ts')):
            if fix_file(os.path.join(root, file)):
                count += 1

print(f"\n✓ Fixed {count} files!")
