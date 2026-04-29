from pydub import AudioSegment
import os


def convert_audio(input_file, output_file):
    """
    将音频文件转换为指定格式
    """
    # 1. 获取文件后缀来判断格式（pydub 通常能自动识别，但指定 format 更稳妥）
    input_format = input_file.split('.')[-1]
    output_format = output_file.split('.')[-1]

    try:
        print(f"正在加载文件: {input_file} ...")
        # 2. 读取音频文件
        # 如果是 mp3 等格式，需要指定 format，如果是 wav 通常可以自动识别
        sound = AudioSegment.from_file(input_file, format=input_format)

        print(f"正在转换并导出: {output_file} ...")
        # 3. 导出文件
        # bitrate 参数用于控制 MP3 的比特率（音质），例如 "128k", "192k", "320k"
        sound.export(output_file, format=output_format, bitrate="192k")

        print("✅ 转换成功！")

    except Exception as e:
        print(f"❌ 转换失败: {e}")

# --- 使用示例 ---
# 将 example.mp3 转换为 example.wav
convert_audio(r"C:\Users\31946\Music\KugouMusic\KugouMusic\星尘 - BBBang.kgg", "example.wav")
# 将 example.wav 转换为 example.mp3
# convert_audio("example.wav", "example.mp3")