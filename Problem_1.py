import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

# 文件路径
file_path_day = 'day.csv'
file_path_hour = 'hour.csv'

# 读取数据
data_day = pd.read_csv(file_path_day)
data_hour = pd.read_csv(file_path_hour)

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
workingday_map = {1: 'Working Day', 0: 'Non-Working Day'}

sns.set(style="whitegrid")

def perform_anova(data):
    """执行ANOVA检验"""
    return stats.f_oneway(
        data[data['season'] == 1]['cnt'],  # 春季
        data[data['season'] == 2]['cnt'],  # 夏季
        data[data['season'] == 3]['cnt'],  # 秋季
        data[data['season'] == 4]['cnt']   # 冬季
    )

def plot_season_usage(data):
    """绘制不同季节的单车使用量分布图"""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=data['season'], y=data['cnt'])
    plt.title('Bike Usage Distribution by Season')
    plt.ylabel('Count')
    plt.xlabel('Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)')
    plt.show()

def t_test(data):
    """执行t检验"""
    workday_data = data[data['weekday'] == 1]['cnt']
    non_workday_data = data[data['weekday'] == 0]['cnt']
    t_stat, p_value = stats.ttest_ind(workday_data, non_workday_data)
    return t_stat, p_value

def plot_hourly_trends(df):
    """绘制每小时的单车使用量趋势图"""
    # 计算每个季节、工作日和非工作日每小时的平均使用量
    df['dteday'] = pd.to_datetime(df['dteday'])
    df_grouped_avg = df.groupby(['season', 'workingday', 'hr'])['cnt'].mean().reset_index()

    # 创建图表
    fig, ax = plt.subplots(figsize=(15, 5))  # 更大的图表
    colors = sns.color_palette("Paired", 8)  # 颜色调色板
    line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':']  # 线条样式

    # 绘制不同季节和工作日/非工作日的趋势
    line_idx = 0  # 线条索引
    for season in range(1, 5):
        for wd in [1, 0]:
            season_wd_data = df_grouped_avg[(df_grouped_avg['season'] == season) & (df_grouped_avg['workingday'] == wd)]
            ax.plot(season_wd_data['hr'], season_wd_data['cnt'],
                    label=f'{season_map[season]} - {workingday_map[wd]}',
                    color=colors[line_idx], linewidth=2, linestyle=line_styles[line_idx])  # 设置颜色和线条样式
            line_idx += 1

    ax.set_title('Average Hourly Usage Trend by Season and Working Day vs Non-Working Day', fontsize=16, fontweight='bold')
    ax.set_xlabel('Hour of the Day', fontsize=14)
    ax.set_ylabel('Average Usage Count', fontsize=14)

    # 设置横轴显示0-23小时
    ax.set_xticks(range(24))
    ax.set_xticklabels([f'{i}' for i in range(24)], fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f'{x:.2f}'))
    ax.legend(title='Season and Day Type', loc='upper left', fontsize=12, title_fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def solve_problem():
    print("Running Problem 1 solution...")

    # 计算按季节的单车使用量平均值
    season_mean_usage = data_day.groupby('season')['cnt'].mean()
    print(season_mean_usage)

    # 执行ANOVA检验
    anova_test = perform_anova(data_day)
    print(anova_test)

    # 绘制季节使用量分布图
    plot_season_usage(data_day)

    # 执行t检验
    t_stat, p_value = t_test(data_day)
    print(f"T-statistic: {t_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("显著差异：工作日与非工作日的单车使用量有显著差异")
    else:
        print("无显著差异：工作日与非工作日的单车使用量没有显著差异")

    # 按小时聚合并输出
    hourly_peak = data_hour.groupby('hr')['cnt'].sum().sort_values(ascending=False)
    print(hourly_peak)

    # 按星期几聚合
    weekday_peak = data_hour.groupby('weekday')['cnt'].sum().sort_values(ascending=False)
    print(weekday_peak)

    # 按季节聚合
    season_peak = data_hour.groupby('season')['cnt'].sum().sort_values(ascending=False)
    print(season_peak)

    # 绘制每小时的单车使用量趋势
    plot_hourly_trends(data_hour)

    print("Problem1 has been solved!")

if __name__ == "__main__":
    solve_problem()
