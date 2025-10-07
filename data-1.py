# -*- coding: utf-8 -*-
import os

os.environ["OMP_NUM_THREADS"] = "1"  # 必须放在所有导入之前

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# -------------------- 高级字体配置 --------------------
try:
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']  # 优先雅黑，备选黑体
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['axes.formatter.use_mathtext'] = True

    # 测试字体
    test_text = "北京保安 电话销售 R²=0.85 工作年限↑"
    plt.figure(figsize=(3, 0.5))
    plt.text(0, 0, test_text)
    plt.axis('off')
    plt.savefig('font_test.png', dpi=50, bbox_inches='tight')
    os.remove('font_test.png')
except Exception as e:
    print(f"字体配置警告: {str(e)}")


# -------------------- 数据加载 --------------------
def load_data():
    file_path = "招聘数据.xlsx"
    df = pd.read_excel(
        file_path,
        sheet_name="Sheet1",
        engine='openpyxl',
        usecols=['城市', '职位', '薪资', '工作经验']
    )
    return df.dropna(subset=['城市', '职位', '薪资']).copy()


# -------------------- 数据预处理 --------------------
def preprocess_data(df):
    def process_salary(s):
        s = str(s).lower().replace('元/月', '').replace('以上', '').replace('以下', '')
        parts = [x for x in s.split('-') if x.replace('.', '').isdigit()]

        try:
            if len(parts) == 1:
                return float(parts[0])
            elif len(parts) >= 2:
                return np.mean([float(parts[0]), float(parts[1])])
        except:
            return np.nan

    experience_map = {
        '不限': 0, '1年以下': 0.5, '1-2年': 1.5,
        '3-5年': 4, '6-7年': 6.5, '8-10年': 9,
        '10年以上': 10
    }

    df['平均薪资'] = df['薪资'].apply(process_salary)
    df['工作经验'] = df['工作经验'].map(experience_map).fillna(0)
    return df.dropna(subset=['平均薪资'])


# -------------------- 分析模块 --------------------
def perform_cluster_analysis(df):
    position_city_matrix = pd.crosstab(df['城市'], df['职位'])
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(position_city_matrix)

    kmeans = KMeans(
        n_clusters=3,
        init='k-means++',
        n_init=20,
        random_state=42
    )

    clusters = kmeans.fit_predict(scaled_data)
    position_city_matrix['Cluster'] = clusters
    return position_city_matrix


def perform_regression_analysis(df):
    X = df[['工作经验']].values.reshape(-1, 1)
    y = df['平均薪资'].values

    model = LinearRegression()
    model.fit(X, y)
    return model, X, y  # 返回模型和数据集


# -------------------- 可视化模块 --------------------
def visualize_results(position_matrix, model, X, y):
    plt.figure(figsize=(18, 7), dpi=100)

    # 聚类热力图
    plt.subplot(1, 2, 1)
    cluster_order = position_matrix.groupby('Cluster').size().sort_values(ascending=False).index
    sns.heatmap(
        position_matrix.groupby('Cluster').mean().loc[cluster_order].T,
        cmap='YlGnBu',
        annot=True,
        fmt=".1f",
        annot_kws={'size': 9},
        cbar_kws={'label': '标准化频数'}
    )
    plt.title('各城市群组的职位分布特征\n(数值表示标准化后的职位占比)', pad=15)
    plt.xlabel('城市群组', labelpad=10)
    plt.ylabel('职位类型', labelpad=10)

    # 回归分析图
    plt.subplot(1, 2, 2)
    ax = sns.regplot(
        x=df['工作经验'],
        y=df['平均薪资'],
        scatter_kws={'alpha': 0.3, 's': 15, 'color': 'steelblue'},
        line_kws={'color': 'crimson', 'lw': 2}
    )

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'¥{x:,.0f}'))
    ax.set_xlim(-0.5, 10.5)

    equation = f'y = {model.coef_[0]:.1f}x + {model.intercept_:.1f}\nR² = {model.score(X, y):.2f}'
    plt.text(
        0.05, 0.9, equation,
        transform=ax.transAxes,
        fontsize=12,
        bbox=dict(facecolor='white', alpha=0.8)
    )

    plt.title('工作经验与薪资关系', pad=15)
    plt.xlabel('工作经验（年）', labelpad=10)
    plt.ylabel('平均月薪', labelpad=10)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# -------------------- 主程序 --------------------
if __name__ == "__main__":
    df = preprocess_data(load_data())

    position_matrix = perform_cluster_analysis(df)
    regression_model, X, y = perform_regression_analysis(df)

    print("\n聚类特征分析：")
    print(position_matrix.groupby('Cluster').mean().T)
    print(f"\n回归分析：每增加1年工作经验，薪资平均增加 {regression_model.coef_[0]:.1f} 元")

    visualize_results(position_matrix, regression_model, X, y)