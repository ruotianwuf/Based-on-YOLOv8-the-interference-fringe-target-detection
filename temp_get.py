import csv
from cnocr import CnOcr
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 定义感兴趣区域的参数
ROI_LEFT = 168  # 左上角横坐标
ROI_TOP = 216   # 左上角纵坐标
ROI_WIDTH = 252  # 宽度
ROI_HEIGHT = 216  # 高度

# 字体设置
FONT_STYLE = ImageFont.truetype("msyhl.ttc", 30, encoding="utf-8")

def predict_get(image):
    ocr = CnOcr(det_model_name='en_PP-OCRv3_det', cand_alphabet='0123456789')
    result = ocr.ocr(image)
    text = result[0]['text']
    print(text)
    return text



def draw_text_on_frame(frame, text, position):
    # 将识别到的文本打印到帧上
    image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image_pil)
    draw.text(position, text, font=FONT_STYLE, fill=(255, 0, 0))  # 红色字体
    return cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

def run_infer(input_video_path, output_csv_path):
    cap = cv2.VideoCapture(input_video_path)
    # 获取视频帧率（FPS）
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps)  # 计算每帧之间的延迟，以毫秒为单位
    print('fps', fps)
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 写入CSV文件的表头
        writer.writerow(["Frame", "Temp"])
        frame_count = 0
        # 逐帧处理视频
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            # 裁剪感兴趣区域
            roi = frame[ROI_TOP:ROI_TOP+ROI_HEIGHT, ROI_LEFT:ROI_LEFT+ROI_WIDTH]
            # 对裁剪后的ROI进行OCR推理
            results = predict_get(roi)
            if results:
                # 在帧上显示识别出的温度
                frame = draw_text_on_frame(frame, results, (50, 50))  # 将文本显示在左上角(50, 50)
            # 显示处理后的帧
            cv2.imshow('number', frame)
            # 按下'Q'键退出
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
            writer.writerow([frame_count, results])

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    input_video_path = 'D:\\AI_Model\\yolov\\Dark_Line_Detector_yolov8\\1080p30fps.mp4'  # 替换为输入视频路径
    output_csv_path = 'D:\\AI_Model\\yolov\\Dark_Line_Detector_yolov8\\output_temp_time.csv'  # 替换为输出CSV文件路径
    run_infer(input_video_path, output_csv_path)
