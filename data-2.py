import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体或其他你系统中存在的中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 数据加载与检查
try:
    # 加载 Excel 文件
    df = pd.read_excel('招聘数据.xlsx')
    print("数据加载成功！")
    print("前5行数据预览：")
    print(df.head())
except Exception as e:
    print(f"加载数据失败，请检查文件路径或格式：{e}")
    exit()

# 2. 数据清洗与转换
def process_salary(salary):
    """
    处理薪资范围，提取最低和最高薪资。
    输入：薪资字符串（如 '10000-30000元/月'）
    输出：最低薪资和最高薪资
    """
    if isinstance(salary, str) and '-' in salary:
        low, high = map(lambda x: int(x.replace('元/月', '')), salary.split('-'))
        return pd.Series([low, high])
    else:
        return pd.Series([np.nan, np.nan])

# 检查是否包含“薪资”列
if '薪资' not in df.columns:
    print("错误：数据中缺少'薪资'列，请检查数据格式。")
    exit()

# 提取薪资范围
salary_cols = df['薪资'].apply(process_salary)
salary_cols.columns = ['薪资_低', '薪资_高']
df = pd.concat([df, salary_cols], axis=1)

# 检查是否包含“城市”列
if '城市' not in df.columns:
    print("错误：数据中缺少'城市'列，请检查数据格式。")
    exit()

# 将城市转换为哑变量
df = pd.get_dummies(df, columns=['城市'], drop_first=True)

# 查看清洗后的数据
print("\n清洗后的数据预览：")
print(df.head())

# 3. 分位数回归分析
# 构建模型公式
formula = '薪资_高 ~ ' + ' + '.join([col for col in df.columns if col.startswith('城市_')])

# 定义分位点
quantiles = [0.1, 0.5, 0.9]

# 拟合分位数回归模型
results = {}
model = smf.quantreg(formula, data=df.dropna())

for qt in quantiles:
    res = model.fit(q=qt)
    results[qt] = res
    print(f"\n分位数 {qt} 的回归结果：")
    print(res.summary())

# 4. 结果可视化
plt.figure(figsize=(10, 6))
for qt, res in results.items():
    params = res.params
    conf = res.conf_int()
    conf['params'] = params
    for idx in conf.index:
        plt.errorbar(qt, params[idx], yerr=[[params[idx] - conf.loc[idx][0]], [conf.loc[idx][1] - params[idx]]], fmt='o')

plt.xlabel('分位数')
plt.ylabel('系数')
plt.title('不同分位数下城市的薪资影响系数')
plt.legend(conf.index, loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
plt.show()