import os

# Paths
modules_dir = r"d:\Machine-Learning-Portfolio\AI_medical_projects\HEALTHWISE-HACKKU25\frontend\src\modules"
ui_dir = r"d:\Machine-Learning-Portfolio\AI_medical_projects\HEALTHWISE-HACKKU25\frontend\src\components\ui"
src_dir = r"d:\Machine-Learning-Portfolio\AI_medical_projects\HEALTHWISE-HACKKU25\frontend\src"

def calculate_relative_path(file_path, src_dir):
    """Calculate correct relative path based on file depth"""
    rel_path = os.path.relpath(file_path, src_dir)
    depth = len(os.path.dirname(rel_path).split(os.sep))
    return "../" * depth

def fix_imports_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Calculate correct relative path for this file
        relative_prefix = calculate_relative_path(filepath, src_dir)
        
        # Fix imports
        content = content.replace('@/components/ui/', f'{relative_prefix}components/ui/')
        content = content.replace('@/lib/utils', f'{relative_prefix}libs/utils')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath} (depth: {relative_prefix})")
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

# Fix all .tsx and .ts files in modules
for root, dirs, files in os.walk(modules_dir):
    for file in files:
        if file.endswith(('.tsx', '.ts')):
            fix_imports_in_file(os.path.join(root, file))

# Fix all .tsx files in UI components  
for file in os.listdir(ui_dir):
    if file.endswith('.tsx'):
        fix_imports_in_file(os.path.join(ui_dir, file))

print("\nDone! All imports fixed with correct depth.")
