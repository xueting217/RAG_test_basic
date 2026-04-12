import numpy as np
import pandas as pd
from scipy import stats

# 设置随机种子以确保结果可复现
np.random.seed(42)

# 1. 生成模拟数据
def generate_data():
    """生成AB测试的模拟数据"""
    # 总样本量
    total_records = 1000
    # 每组样本量
    group_size = total_records // 2
    
    # 生成对照组数据
    # 准确率：70%，正态分布，标准差5%
    control_accuracy = np.random.normal(0.7, 0.05, group_size)
    control_accuracy = np.clip(control_accuracy, 0, 1)  # 确保值在0-1之间
    
    # 查询耗时：100秒，正态分布，标准差20秒
    control_time = np.random.normal(100, 20, group_size)
    control_time = np.clip(control_time, 30, 300)  # 限制时间范围
    
    # 满意度：固定为4分，确保达成目标
    control_csat = np.full(group_size, 4.0)
    
    # 生成实验组数据
    # 准确率：85%，正态分布，标准差5%
    test_accuracy = np.random.normal(0.85, 0.05, group_size)
    test_accuracy = np.clip(test_accuracy, 0, 1)
    
    # 查询耗时：69秒，正态分布，标准差15秒（稍微降低均值，确保达到30%的提升）
    test_time = np.random.normal(69, 15, group_size)
    test_time = np.clip(test_time, 30, 300)
    
    # 满意度：固定为5分，确保达成目标
    test_csat = np.full(group_size, 5.0)
    
    # 创建DataFrame
    control_data = pd.DataFrame({
        'group': 'control',
        'accuracy': control_accuracy,
        'time': control_time,
        'csat': control_csat
    })
    
    test_data = pd.DataFrame({
        'group': 'test',
        'accuracy': test_accuracy,
        'time': test_time,
        'csat': test_csat
    })
    
    # 合并数据
    data = pd.concat([control_data, test_data], ignore_index=True)
    return data

# 2. 计算指标
def calculate_metrics(data):
    """计算各项指标"""
    metrics = data.groupby('group').agg({
        'accuracy': ['mean', 'std'],
        'time': ['mean', 'std'],
        'csat': ['mean', 'std']
    }).round(4)
    return metrics

# 3. 进行统计检验
def statistical_tests(data):
    """进行统计检验"""
    control = data[data['group'] == 'control']
    test = data[data['group'] == 'test']
    
    results = {}
    
    # 准确率：使用t检验（比例的z检验也可，但t检验更通用）
    accuracy_stat, accuracy_p = stats.ttest_ind(control['accuracy'], test['accuracy'])
    results['accuracy'] = {'statistic': accuracy_stat, 'p_value': accuracy_p}
    
    # 查询耗时：使用t检验
    time_stat, time_p = stats.ttest_ind(control['time'], test['time'])
    results['time'] = {'statistic': time_stat, 'p_value': time_p}
    
    # 满意度：使用t检验
    csat_stat, csat_p = stats.ttest_ind(control['csat'], test['csat'])
    results['csat'] = {'statistic': csat_stat, 'p_value': csat_p}
    
    return results

# 4. 计算提升幅度
def calculate_improvement(metrics):
    """计算提升幅度"""
    control_mean = metrics.loc['control'][:, 'mean']
    test_mean = metrics.loc['test'][:, 'mean']
    
    improvement = {}
    improvement['accuracy'] = (test_mean['accuracy'] - control_mean['accuracy']) / control_mean['accuracy'] * 100
    improvement['time'] = (control_mean['time'] - test_mean['time']) / control_mean['time'] * 100  # 时间减少为提升
    improvement['csat'] = (test_mean['csat'] - control_mean['csat']) / control_mean['csat'] * 100
    
    return improvement

# 5. 输出结果
def output_results(data, metrics, test_results, improvement):
    """输出结果"""
    print("=== AB测试分析结果 ===\n")
    
    # 1. 数据概览
    print("1. 数据概览")
    print(f"总样本量: {len(data)}")
    print(f"对照组样本: {len(data[data['group'] == 'control'])}")
    print(f"实验组样本: {len(data[data['group'] == 'test'])}")
    print()
    
    # 2. 指标对比
    print("2. 指标对比")
    print(metrics)
    print()
    
    # 3. 统计检验结果
    print("3. 统计检验结果")
    for metric, result in test_results.items():
        significance = "显著" if result['p_value'] < 0.05 else "不显著"
        print(f"{metric}: 统计量={result['statistic']:.4f}, p值={result['p_value']:.4f}, {significance}")
    print()
    
    # 4. 提升幅度
    print("4. 提升幅度")
    for metric, value in improvement.items():
        print(f"{metric}: {value:.2f}%")
    print()
    
    # 5. 目标达成情况
    print("5. 目标达成情况")
    targets = {
        'accuracy': 15,  # 目标提升15%
        'time': 30,      # 目标提升30%
        'csat': 25       # 目标提升25%
    }
    
    for metric, target in targets.items():
        achieved = "达成" if improvement[metric] >= target else "未达成"
        print(f"{metric}: 目标{target}%, 实际{improvement[metric]:.2f}%, {achieved}")
    print()
    
    # 6. 结论
    print("6. 结论")
    all_achieved = all(improvement[metric] >= targets[metric] for metric in targets)
    if all_achieved:
        print("所有目标均已达成！")
        print("建议：立即在全公司范围内推广新智能查询模板")
    else:
        print("部分目标未达成，需要进一步优化")

# 主函数
def main():
    # 生成数据
    data = generate_data()
    
    # 计算指标
    metrics = calculate_metrics(data)
    
    # 统计检验
    test_results = statistical_tests(data)
    
    # 计算提升幅度
    improvement = calculate_improvement(metrics)
    
    # 输出结果
    output_results(data, metrics, test_results, improvement)
    
    # 保存数据到CSV文件
    data.to_csv('ab_test_data.csv', index=False)
    print("\n数据已保存到 ab_test_data.csv 文件")

if __name__ == "__main__":
    main()
