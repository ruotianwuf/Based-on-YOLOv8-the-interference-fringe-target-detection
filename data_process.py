import csv
import matplotlib.pyplot as plt

def calculate_average_height(input_csv_path):
    heights = []
    with open(input_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头

        for row in reader:
            height = int(row[7])  # 假设height在第8列（索引从0开始，因此索引为7）
            heights.append(height)

    average_height = sum(heights) / len(heights) if heights else 0
    return average_height

def process_y_data(input_csv_path, average_height, output_csv_path):
    with open(input_csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # 读取表头
        rows = list(reader)  # 读取所有数据行

    y_values = [int(row[3]) for row in rows]  # 提取所有的Y坐标值（假设Y1在第4列）
    temperatures = [float(row[8]) for row in rows]  # 提取所有的温度值（假设温度在第9列）

    # 处理重复温度数据，确保每个温度值有所不同，且最高不超过47.0
    temp_count = {}
    adjusted_temperatures = []

    for temp in temperatures:
        if temp in temp_count:
            temp_count[temp] += 1
            increment = temp_count[temp] * 0.0001  # 使用更小的增量
            adjusted_temp = temp + increment
            if adjusted_temp >= 47.0:
                adjusted_temp = 47.0 - increment  # 确保最高不超过47.0
        else:
            temp_count[temp] = 0
            adjusted_temp = temp

        adjusted_temperatures.append(round(adjusted_temp, 4))

    change_count = 0
    dark_to_light_count = 0  # 暗变明次数
    light_to_dark_count = 0  # 明变暗次数
    start_value = y_values[0]  # 第一个定位值
    previous_temperature = adjusted_temperatures[0]  # 初始化“变化前的温度”

    temperature_list = []  # 用于存储对应的温度
    stripe_changes = []  # 用于存储条纹变化次数

    for i in range(1, len(y_values)):
        current_value = y_values[i]
        diff = current_value - start_value
        abs_diff = abs(diff)

        current_temperature = adjusted_temperatures[i]
        current_frame_rate = rows[i][0]  # 假设帧率在第1列

        if abs_diff >= average_height - 10 and abs_diff <= average_height + 30:
            change_count += 1
            temperature_list.append(current_temperature)  # 记录温度变化
            stripe_changes.append(change_count)

            if diff < 0:
                dark_to_light_count += 1
                print(f"变化 {change_count}: 参考值 = {start_value}, 当前值 = {current_value}, "
                      f"差值 = {diff}，暗变明，温度 = {current_temperature}, 变化前的温度 = {previous_temperature}, 帧率 = {current_frame_rate}")
            elif diff > 0:
                light_to_dark_count += 1
                print(f"变化 {change_count}: 参考值 = {start_value}, 当前值 = {current_value}, "
                      f"差值 = {diff}，明变暗，温度 = {current_temperature}, 变化前的温度 = {previous_temperature}, 帧率 = {current_frame_rate}")

            # 更新定位的值和“变化前的温度”
            start_value = current_value
            previous_temperature = current_temperature
        elif abs_diff > 400 and abs_diff < 550:  # 如果变化超过400，则判定为新数据
            start_value = current_value
            previous_temperature = current_temperature
            print(f"发现新数据，定位值更新为: {start_value}, 温度 = {current_temperature}, 帧率 = {current_frame_rate}")

    print(f"总计检测到 {change_count} 次变化")
    print(f"暗变明次数: {dark_to_light_count}")
    print(f"明变暗次数: {light_to_dark_count}")

    # 保存调整后的温度和条纹变化数据到CSV文件
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Temperature', 'Stripe Change Count'])
        writer.writerows(zip(temperature_list, stripe_changes))

    return temperature_list, stripe_changes

def plot_relationship(temperatures, stripe_changes, output_image_path):
    plt.figure(figsize=(10, 6))

    # 绘制关系曲线
    plt.plot(temperatures, stripe_changes, marker='o', color='blue')

    plt.xlabel('Temperature')
    plt.ylabel('Stripe Change Count')
    plt.title('Relationship between Temperature and Stripe Change Count')

    plt.grid(True)

    # 设置横坐标从30开始
    plt.xlim(left=30)

    # 设置横坐标刻度间隔
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    step = 1  # 设置刻度间隔为1
    plt.xticks([round(x, 1) for x in list(frange(30, max_temp + step, step))])

    plt.savefig(output_image_path)  # 保存图表
    plt.show()

def frange(start, stop, step):
    while start < stop:
        yield round(start, 1)
        start += step

# 使用示例
input_csv_path = 'processed_output_positions_3.csv'  # 输入处理后的CSV文件路径
output_csv_path = 'adjusted_output.csv'  # 输出调整后的CSV文件路径
output_image_path = 'relationship_plot.png'  # 输出图表的PNG文件路径

# 计算平均框高
average_height = calculate_average_height(input_csv_path)
print(f"计算得到的平均框高: {average_height:.2f}")

# 处理Y轴数据并获取变化信息
temperatures, stripe_changes = process_y_data(input_csv_path, average_height, output_csv_path)

# 绘制条纹变化和温度变化的关系图并保存
plot_relationship(temperatures, stripe_changes, output_image_path)
