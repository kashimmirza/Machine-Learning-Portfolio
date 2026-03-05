import os
import re

# Paths
modules_dir = r"d:\Machine-Learning-Portfolio\AI_medical_projects\HEALTHWISE-HACKKU25\frontend\src\modules"
ui_dir = r"d:\Machine-Learning-Portfolio\AI_medical_projects\HEALTHWISE-HACKKU25\frontend\src\components\ui"

def fix_imports_in_file(filepath, is_module=True):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        if is_module:
            # For module files: @/components/ui → ../../components/ui
            content = content.replace('@/components/ui/', '../../components/ui/')
            content = content.replace('@/lib/utils', '../../libs/utils')
        else:
            # For UI component files: @/lib/utils → ../../libs/utils
            content = content.replace('@/lib/utils', '../../libs/utils')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")

# Fix all .tsx and .ts files in modules
for root, dirs, files in os.walk(modules_dir):
    for file in files:
        if file.endswith(('.tsx', '.ts')):
            fix_imports_in_file(os.path.join(root, file), is_module=True)

# Fix all .tsx files in UI components
for file in os.listdir(ui_dir):
    if file.endswith('.tsx'):
        fix_imports_in_file(os.path.join(ui_dir, file), is_module=False)

print("\nDone! All imports fixed.")
