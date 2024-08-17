import csv

def process_y_coordinates(input_csv_path, output_csv_path):
    # 读取CSV文件中的数据
    with open(input_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头
        rows = list(reader)  # 读取所有数据行

    # 初始化处理后的数据列表
    processed_rows = []

    # 遍历所有数据行
    for i in range(1, len(rows)):
        previous_row = rows[i-1]
        current_row = rows[i]

        # 获取前一个和当前Y坐标值
        y_previous = previous_row[3]  # Y1在第4列
        y_current = current_row[3]

        # 检查Y值是否为空
        if not y_current or not y_previous:
            print("Y值为空，删除当前行")
            continue  # 如果Y值为空，跳过这行数据

        y_previous = int(y_previous)
        y_current = int(y_current)

        # 计算Y坐标差值
        y_diff = abs(y_current - y_previous)

        # 判断差距并决定是否删除当前行
        if 50 < y_diff <= 400:
            print("大于50小于400，判定为识别错误")
        else:
            processed_rows.append(current_row)
        # 如果差距大于400，不删除当前行，直接跳过继续处理

    # 将处理后的数据写入新的CSV文件
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # 写入表头
        writer.writerows(processed_rows)  # 写入处理后的数据

    print(f"数据处理完成，结果已保存到 {output_csv_path}")

if __name__ == '__main__':
    input_csv_path = 'output_positions_3.csv'  # 输入CSV文件路径
    output_csv_path = 'processed_output_positions_3.csv'  # 输出CSV文件路径
    process_y_coordinates(input_csv_path, output_csv_path)
