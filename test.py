import pygame
import os

pygame.mixer.init()

# 遍历 music 文件夹中的所有音频文件
music_dir = "music"
extensions = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']

if not os.path.exists(music_dir):
    print(f"Error: Directory '{music_dir}' does not exist!")
    exit(1)

# 获取所有音频文件
audio_files = []
for filename in os.listdir(music_dir):
    if any(filename.lower().endswith(ext) for ext in extensions):
        audio_files.append(filename)

if not audio_files:
    print(f"No audio files found in '{music_dir}' directory!")
    exit(1)

print(f"Found {len(audio_files)} audio file(s) in '{music_dir}':")
print("=" * 60)

# 测试每个文件
valid_files = []
invalid_files = []

for i, filename in enumerate(audio_files, 1):
    file_path = os.path.join(music_dir, filename)
    try:
        pygame.mixer.music.load(file_path)
        print(f"✓ File {i}: {filename} - OK")
        valid_files.append(filename)
    except Exception as e:
        print(f"✗ File {i}: {filename} - ERROR: {e}")
        invalid_files.append(filename)

print("=" * 60)
print(f"\nSummary:")
print(f"  Valid files:   {len(valid_files)}")
print(f"  Invalid files: {len(invalid_files)}")

if valid_files:
    print(f"\nValid files:")
    for f in valid_files:
        print(f"  - {f}")

if invalid_files:
    print(f"\nInvalid files (need conversion):")
    for f in invalid_files:
        print(f"  - {f}")
