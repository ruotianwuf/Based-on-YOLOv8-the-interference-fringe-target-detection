import os
import json
from ultralytics import YOLO

y_address = []


def extract_points_from_json(folder_path):
    heights = []
    height_records = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                if 'shapes' in data and len(data['shapes']) > 0:
                    for shape in data['shapes']:
                        if 'points' in shape and len(shape['points']) == 4:
                            y_address.append(shape['points'][3][1])
                            height = abs(shape['points'][2][1] - shape['points'][0][1])
                            heights.append(height)
                            height_records.append({
                                'filename': filename,
                                'height': height
                            })

    return heights, height_records


def calculate_average_height(heights):
    if heights:
        average_height = sum(heights) / len(heights)
        return average_height
    else:
        return None


def detect_height_changes(height_records, average_height):
    change_count = 0
    previous_height = None

    for record in height_records:
        current_height = record['height']

        if previous_height is not None:
            height_diff = abs(current_height - previous_height)
            if height_diff > average_height:
                change_count += 1
                print(f"变化 {change_count}: {record['filename']}, 高度差: {height_diff:.2f}")

        previous_height = current_height

    return change_count


def analyze_data_and_train_model(folder_path, data_yaml, epochs=300, batch_size=4, imgsz=640):
    # 数据分析
    heights, height_records = extract_points_from_json(folder_path)
    average_height = calculate_average_height(heights)
    print(f"所有框的平均高度: {average_height:.2f}")
    # 检测暗变明和明变暗次数
    data = y_address
    count = 0
    dark_to_light_count = 0
    light_to_dark_count = 0
    reference_value = data[0]

    for i in range(1, len(data)):
        current_value = data[i]
        difference = current_value - reference_value

        if abs(difference) >= average_height:
            count += 1
            if difference < 0:
                dark_to_light_count += 1
                print(
                    f"变化 {count}: 参考值 = {reference_value}, 当前值 = {current_value}, 差值 = {difference:.2f}，暗变明")
            elif difference > 0:
                light_to_dark_count += 1
                print(
                    f"变化 {count}: 参考值 = {reference_value}, 当前值 = {current_value}, 差值 = {difference:.2f}，明变暗")
            reference_value = current_value

    print(f"总计检测到 {count} 次变化")
    print(f"暗变明次数: {dark_to_light_count}")
    print(f"明变暗次数: {light_to_dark_count}")

    # 加载预训练模型并训练
    model = YOLO('yolov8n.pt')  # 加载预训练模型
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        name='dark_detection',
        device='0',
        lr0=0.001,  # 初始学习率
        lrf=0.01,
        amp=True,
        augment=True,  # 启用数据增强
        flipud=0.2,  # 例如，垂直翻转的概率
        fliplr=0.3,  # 水平翻转的概率
        mosaic=1.0,  # 使用马赛克数据增强
        mixup=0.3
    )

    # 打印训练结果
    try:
        print("Training Results:", results)
    except:
        print("no result")



if __name__ == '__main__':
    folder_path = 'D:\\AI_Model\\yolov\\Dark_Line_Detector_yolov8\\data\\json_file'  # 替换为你的文件夹路径
    data_yaml = 'dataset.yaml'  # 替换为你的数据集yaml文件路径
    analyze_data_and_train_model(folder_path, data_yaml)
