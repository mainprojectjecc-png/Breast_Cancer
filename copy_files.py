import shutil
import os

src_dir = 'finalminiproject-main'
dest_dir = '.'

# Copy all Python, text, and config files
for f in os.listdir(src_dir):
    full_path = os.path.join(src_dir, f)
    if os.path.isfile(full_path) and f.endswith(('.py', '.txt', '.md', '.html', '.css')):
        shutil.copy(full_path, os.path.join(dest_dir, f))
        print(f'Copied: {f}')

# Copy models directory
models_src = os.path.join(src_dir, 'models')
models_dest = os.path.join(dest_dir, 'models')
if os.path.exists(models_src):
    shutil.copytree(models_src, models_dest, dirs_exist_ok=True)
    print(f'Copied: models directory')

print('✓ All files copied successfully!')
