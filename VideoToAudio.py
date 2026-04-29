import os
import tqdm
from moviepy import VideoFileClip

# 定义支持的视频格式后缀
SUPPORTED_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv']


class AudioConverter:
    def __init__(self, input_folder: str = None, output_folder: str = None):
        self.video_list = []
        self.format_list = []
        self.input_folder = input_folder or r"C:\Users\31946\Videos\Captures"
        self.output_folder = output_folder or r"C:\Users\31946\Videos\Common\Try"

        # 确保输出目录存在
        os.makedirs(self.output_folder, exist_ok=True)

    def scan_folder(self, folder_path: str = None):
        """扫描指定文件夹下的视频文件"""
        if folder_path is None:
            folder_path = self.input_folder

        if not os.path.exists(folder_path):
            print(f"错误：文件夹不存在 -> {folder_path}")
            return []

        print(f"正在扫描文件夹: {folder_path} ...")
        found_files = []

        for filename in os.listdir(folder_path):
            _, ext = os.path.splitext(filename)
            if ext.lower() in SUPPORTED_FORMATS:
                name_without_ext = os.path.splitext(filename)[0]
                found_files.append((name_without_ext, ext.lower()))

        found_files.sort()

        print(f"发现 {len(found_files)} 个视频文件：")
        for i, (name, ext) in enumerate(found_files):
            print(f"  [{i + 1}] {name}{ext}")

        return found_files

    def set_videos(self, video_data):
        """接收扫描结果并赋值给内部变量"""
        if not video_data:
            print("没有设置视频列表")
            return

        self.video_list = [item[0] for item in video_data]
        self.format_list = [item[1] for item in video_data]

    def get_file_size_mb(self, file_path: str) -> float:
        return os.path.getsize(file_path) / (1024 * 1024)

    def convert_videos_to_audio(self):
        """使用 MoviePy (兼容 2.0+ 版本) 执行批量转换"""
        if not self.video_list:
            print("列表为空，请先扫描或设置视频。")
            return

        print(f"\n开始转换，共 {len(self.video_list)} 个文件...\n")
        success_count = 0

        # --- 修改点 1: 引入 tqdm 进度条 ---
        # desc 是进度条前的描述，unit 是单位
        from tqdm import tqdm
        for i, video_name in tqdm(enumerate(self.video_list), desc="总体进度", unit="个"):

            ext = self.format_list[i]
            input_path = os.path.join(self.input_folder, video_name + ext)

            # 输出文件名逻辑
            input_size_mb = self.get_file_size_mb(input_path)
            output_ext = ".mp3" if input_size_mb > 512 else ".wav"
            output_path = os.path.join(self.output_folder, video_name + output_ext)

            # --- 修改点 2: 移除 print，改用 tqdm.set_description ---
            # 这样不会刷屏，而是动态更新进度条后的文字
            tqdm.write(f"正在处理: {video_name}{ext}")

            try:
                # --- 加载视频 ---
                clip = VideoFileClip(input_path)

                if clip.audio is None:
                    tqdm.write(f"   ✗ 失败: 该视频文件没有音频轨道")
                    clip.close()
                    continue

                audio_clip = clip.audio

                # --- 写入音频文件 ---
                codec = 'libmp3lame' if output_ext == '.mp3' else 'pcm_s16le'

                # --- 修改点 3: 开启 MoviePy 内部进度条 ---
                # logger='bar' 会显示当前文件的具体处理进度（如 10%... 50%...）
                audio_clip.write_audiofile(output_path, codec=codec, logger="bar")

                # --- 释放资源 ---
                clip.close()

                # 计算统计信息
                out_size = self.get_file_size_mb(output_path)
                ratio = (1 - out_size / input_size_mb) * 100

                tqdm.write(f"   ✓ 成功 | 输入: {input_size_mb:.2f}MB, 输出: {out_size:.2f}MB, 压缩率: {ratio:.1f}%")
                success_count += 1

            except Exception as e:
                tqdm.write(f"   ✗ 失败: {e}")

        print(f"\n全部完成！成功: {success_count}, 失败: {len(self.video_list) - success_count}")

# 主程序入口
if __name__ == "__main__":
    converter = AudioConverter(
        input_folder=r"C:\Users\31946\Videos\屏幕录制",
        output_folder=r"C:\Users\31946\Videos\Common\Try"
    )

    # 1. 扫描
    video_data = converter.scan_folder()

    # 2. 设置
    if video_data:
        converter.set_videos(video_data)
        # 3. 转换
        converter.convert_videos_to_audio()
    else:
        print("未找到视频文件，程序退出。")