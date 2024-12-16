import pandas as pd
import matplotlib
matplotlib.use('TkAgg')

file_path_day = 'day.csv'
file_path_hour = 'hour.csv'

# 读取数据
data = pd.read_csv(file_path_day)

def solve_problem():
    # 提取不同天气状态的数据
    weather_data = {
        'Good Weather': data[data['weathersit'] == 1]['cnt'],  # 天气较好
        'Moderate Weather': data[data['weathersit'] == 2]['cnt'],  # 中等天气
        'Bad Weather': data[data['weathersit'] == 3]['cnt'],  # 天气较差
    }

    # 查看每种天气状态的单车使用量的均值
    for weather, usage in weather_data.items():
        print(f"{weather} 时单车使用量的均值: {usage.mean():.2f}")

    from scipy.stats import kruskal

    # Kruskal-Wallis检验
    h_stat, p_value = kruskal(weather_data['Good Weather'],
                              weather_data['Moderate Weather'],
                              weather_data['Bad Weather'])
    print(f"Kruskal-Wallis H-statistic: {h_stat:.2f}, p-value: {p_value:.4f}")

    # 判断显著性
    if p_value < 0.05:
        print("不同天气状态下单车使用量的中位数存在显著差异。")
    else:
        print("不同天气状态下单车使用量的中位数没有显著差异。")
