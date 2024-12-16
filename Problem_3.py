import pandas as pd
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import matplotlib
from statsmodels.stats.proportion import proportions_ztest

matplotlib.use('TkAgg')

file_path_day = 'day.csv'
file_path_hour = 'hour.csv'

# 读取数据
data = pd.read_csv(file_path_day)

def plot_stacked_bar(data):
    """绘制堆叠条形图"""
    # 按工作日分组计算平均使用量
    workingday_data = data.groupby('workingday')[['casual', 'registered']].mean().reset_index()
    workingday_data['workingday'] = workingday_data['workingday'].map({0: 'Non-Working Day', 1: 'Working Day'})

    plt.figure(figsize=(8, 8), dpi=300)
    plt.bar(workingday_data['workingday'], workingday_data['registered'], label='Registered Users', color='skyblue')
    plt.bar(workingday_data['workingday'], workingday_data['casual'], bottom=workingday_data['registered'],
            label='Casual Users', color='lightcoral')
    plt.title('Bike Usage on Working vs Non-Working Days')
    plt.ylabel('Average Daily Usage')
    plt.xlabel('Day Type')
    plt.legend()
    plt.tight_layout()
    plt.show()


def calculate_workingday_statistics(data):
    """计算工作日和非工作日的统计数据并进行Z检验"""
    workingday_data = data.groupby('workingday')[['casual', 'registered']].sum().reset_index()
    workingday_data['total'] = workingday_data['casual'] + workingday_data['registered']
    workingday_data['casual_ratio'] = workingday_data['casual'] / workingday_data['total']
    workingday_data['workingday'] = workingday_data['workingday'].map({0: 'Non-Working Day', 1: 'Working Day'})

    print(workingday_data[['workingday', 'casual_ratio']])

    # 进行两比例Z检验
    count = workingday_data['casual'].values
    nobs = workingday_data['total'].values
    z_stat, p_value = proportions_ztest(count, nobs)

    print(f"Z-statistic: {z_stat:.2f}, p-value: {p_value:.8f}")
    return p_value


def chi_square_test_and_plot(data):
    """进行卡方检验并绘制堆叠条形图"""
    weather_usage = data.groupby('weathersit')[['casual', 'registered']].mean().reset_index()
    weather_usage['weathersit'] = weather_usage['weathersit'].map({
        1: 'Good Weather',
        2: 'Moderate Weather',
        3: 'Bad Weather',
        4: 'Severe Weather'
    })

    print(weather_usage)

    # 构建列联表
    contingency_table = pd.DataFrame({
        'Good Weather': [964, 3913],
        'Moderate Weather': [687, 3349],
        'Bad Weather': [185, 1618]
    }, index=['Casual Users', 'Registered Users'])

    print("Contingency Table:")
    print(contingency_table)

    # 进行chi-square检验
    chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

    print(f"Chi-square statistic: {chi2_stat:.2f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Degrees of freedom: {dof}")
    print("Expected frequencies:")
    print(pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))

    if p_value < 0.05:
        print("拒绝原假设：注册用户和非注册用户的使用占比在不同天气下存在显著差异。")
    else:
        print("不能拒绝原假设：注册用户和非注册用户的使用占比在不同天气下没有显著差异。")

    # 绘制堆叠条形图
    contingency_table_percent = contingency_table.div(contingency_table.sum(axis=0), axis=1) * 100
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    contingency_table_percent.T.plot(kind='bar', stacked=True, color=['lightcoral', 'skyblue'], ax=ax)

    plt.title('Proportion of Casual vs Registered Users Across Weather Conditions')
    plt.ylabel('Percentage (%)')
    plt.xlabel('Weather Condition')
    plt.legend(title='User Type')
    plt.tight_layout()
    plt.show()

def solve_problem():
    plot_stacked_bar(data)

    # 进行工作日/非工作日比例Z检验
    p_value = calculate_workingday_statistics(data)
    if p_value < 0.05:
        print("非注册用户在非工作日的使用比例显著高于工作日。")
    else:
        print("非注册用户在非工作日的使用比例与工作日没有显著差异。")

    chi_square_test_and_plot(data)

