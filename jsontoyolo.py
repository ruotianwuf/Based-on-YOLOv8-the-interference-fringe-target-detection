import json
import os

# 指定包含JSON文件的文件夹路径
json_folder_path = '/data/json_file'  # 替换为包含JSON文件的文件夹路径
output_dir = '/dataset/labels/train'  # 替换为你想要保存YOLO格式标签的路径

os.makedirs(output_dir, exist_ok=True)

# 遍历文件夹中的所有JSON文件
for filename in os.listdir(json_folder_path):
    if filename.endswith('.json'):
        json_file_path = os.path.join(json_folder_path, filename)

        # 读取JSON文件
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # 提取图像信息
        image_width = data['imageWidth']
        image_height = data['imageHeight']

        # 遍历标注的形状
        for shape in data['shapes']:
            label = shape['label']  # 标签类别
            points = shape['points']  # 矩形的四个角点

            # 计算矩形边界框
            x_min = min(points[0][0], points[1][0])
            x_max = max(points[0][0], points[1][0])
            y_min = min(points[0][1], points[2][1])
            y_max = max(points[0][1], points[2][1])

            # 计算中心点、宽度和高度
            x_center = (x_min + x_max) / 2.0 / image_width
            y_center = (y_min + y_max) / 2.0 / image_height
            bbox_width = (x_max - x_min) / image_width
            bbox_height = (y_max - y_min) / image_height

            # YOLO格式：<class_id> <x_center> <y_center> <width> <height>
            yolo_format = f"0 {x_center} {y_center} {bbox_width} {bbox_height}\n"  # 假设类别ID为0

            # 保存为YOLO格式文件
            output_file_path = os.path.join(output_dir, os.path.splitext(data['imagePath'])[0] + '.txt')
            with open(output_file_path, 'w') as out_file:
                out_file.write(yolo_format)

        print(f"JSON文件已成功转换为YOLO格式: {filename}")

print(f"所有JSON文件已成功转换为YOLO格式，并保存到: {output_dir}")
