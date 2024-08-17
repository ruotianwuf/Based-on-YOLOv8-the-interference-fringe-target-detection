import cv2
import csv
from ultralytics import YOLO

def run_inference_and_save_to_csv(model_path, input_video_path, output_csv_path):
    # 加载训练好的模型
    model = YOLO(model_path)

    # 打开输入视频
    cap = cv2.VideoCapture(input_video_path)

    # 获取视频帧率（FPS）
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    delay = int(1000 / fps)  # 计算每帧之间的延迟，以毫秒为单位
    print('fps', fps)
    # 准备CSV文件
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        # 写入CSV文件的表头
        writer.writerow(["Frame", "Conf", "X1", "Y1", "X2", "Y2", "Width", "Height"])

        frame_count = 0

        # 逐帧处理视频
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # 对每一帧进行推理
            results = model(frame)

            # 检查是否有检测结果
            if len(results[0].boxes) > 0:
                # 初始化最大置信度和对应的框
                max_conf = -1
                max_conf_box = None

                # 遍历所有检测框，找到置信度最高的框
                for box in results[0].boxes:
                    if box.conf > max_conf:
                        max_conf = box.conf
                        max_conf_box = box

                if max_conf_box is not None:
                    # 获取位置信息（左上角x, 左上角y, 宽度, 高度）
                    x1, y1, x2, y2 = max_conf_box.xyxy[0]  # 获取边界框的坐标
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    width = x2 - x1
                    height = y2 - y1

                    # 将置信度转换为浮点数
                    conf_value = max_conf_box.conf.item()

                    # 写入CSV文件
                    writer.writerow([frame_count, conf_value, x1, y1, x2, y2, width, height])

                    # 在帧上绘制置信度最高的检测框
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # 标注位置参数和置信度
                    label = f"Conf: {conf_value:.2f}, Pos: ({x1},{y1}), W:{width}, H:{height}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            else:
                # 如果没有检测到任何结果，写入None
                writer.writerow([frame_count, None, None, None, None, None, None, None])

            # 显示结果
            cv2.imshow('YOLOv8 Inference', frame)

            # 按下'Q'键退出
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

    # 释放视频对象
    cap.release()
    cv2.destroyAllWindows()

    print(f"推理完成并保存到 {output_csv_path}")


if __name__ == '__main__':
    model_path = 'D:\\AI_Model\\yolov\\Dark_Line_Detector_yolov8\\runs\\detect\\dark_detection2\\weights\\best.pt'  # 替换为你的模型路径
    input_video_path = '截帧视频.mp4'  # 替换为输入视频路径
    output_csv_path = 'output_positions_3.csv'  # 替换为输出CSV文件路径

    run_inference_and_save_to_csv(model_path, input_video_path, output_csv_path)
