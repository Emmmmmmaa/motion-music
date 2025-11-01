"""
将音乐文件转换为 pygame 兼容的格式
使用 pydub (需要安装 ffmpeg)
"""
import os
from pydub import AudioSegment

def convert_to_compatible_mp3(input_file, output_file=None):
    """转换 MP3 文件为 pygame 兼容格式"""
    if output_file is None:
        # 创建输出文件名（添加 _converted 后缀）
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_converted{ext}"
    
    try:
        print(f"Converting {input_file}...")
        # 加载音频文件
        audio = AudioSegment.from_file(input_file)
        
        # 导出为标准的 MP3 格式
        audio.export(output_file, format="mp3", bitrate="192k")
        print(f"Successfully converted to: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error converting {input_file}: {e}")
        return None

def convert_music_directory(music_dir="music"):
    """转换目录中的所有 MP3 文件"""
    if not os.path.exists(music_dir):
        print(f"Directory {music_dir} does not exist!")
        return
    
    converted_files = []
    for filename in os.listdir(music_dir):
        if filename.lower().endswith('.mp3'):
            file_path = os.path.join(music_dir, filename)
            # 跳过已经转换过的文件
            if '_converted' not in filename:
                output_file = convert_to_compatible_mp3(file_path)
                if output_file:
                    converted_files.append(output_file)
    
    if converted_files:
        print(f"\nConverted {len(converted_files)} files successfully!")
        print("You can now use the _converted.mp3 files in your project.")
    else:
        print("No files converted.")

if __name__ == "__main__":
    print("Music File Converter for pygame")
    print("=" * 40)
    print("Note: This requires pydub and ffmpeg")
    print("Install: pip install pydub")
    print("Install ffmpeg: brew install ffmpeg (Mac) or apt-get install ffmpeg (Linux)")
    print("=" * 40)
    
    convert_music_directory()

