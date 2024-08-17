import cv2
import os
import numpy as np

def extract_frames_with_temperature(video_path, output_folder, start_temp, end_temp, frame_interval=30):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    # 获取视频的总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 计算每一帧对应的温度
    temperatures = np.linspace(start_temp, end_temp, total_frames)

    frame_count = 0

    while True:
        ret, frame = cap.read()

        # 如果视频读取完毕，退出循环
        if not ret:
            break

        # 仅在当前帧是指定间隔的倍数时保存图片
        if frame_count % frame_interval == 0:
            # 当前帧的温度
            current_temp = temperatures[frame_count]

            # 生成每一帧的文件名，带上温度信息
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:06d}_{current_temp:.2f}C.jpg")

            # 保存帧图像
            cv2.imwrite(frame_filename, frame)

            print(f"保存 {frame_filename}")

        frame_count += 1

    # 释放视频捕获对象
    cap.release()
    print("视频处理完成")

# 示例调用
video_path = "截帧视频.mp4"  # 替换为你的视频文件路径
output_folder = "extracted_frames"  # 替换为你想保存帧图片的文件夹路径
start_temp = 30  # 起始温度
end_temp = 47    # 结束温度

extract_frames_with_temperature(video_path, output_folder, start_temp, end_temp)
