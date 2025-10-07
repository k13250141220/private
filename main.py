import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

# CSV文件列表
csv_files = ['小说.csv', '传记.csv', '历史.csv','推理.csv','漫画.csv','科普.csv','网络小说.csv']
all_data = pd.DataFrame()

# 读取并合并所有CSV文件
for file in csv_files:
    df = pd.read_csv(file)
    all_data = pd.concat([all_data, df], ignore_index=True)

# 保存合并后的数据到新CSV文件
all_data.to_csv('豆瓣图书.csv', index=False)

# 设置字体属性以支持 CJK 字符
rcParams['font.sans-serif'] = ['SimHei'] # SimHei is a common font for Chinese text
rcParams['axes.unicode_minus'] = False # Enable negative signs
# 书籍数据
df = pd.read_csv('豆瓣图书.csv')

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# 数据概览
print(df.head()) # 查看前几行数据

# 评分分布
plt.hist(df['评分'], bins=20, color='blue', edgecolor='black') # 修改这里将bins参数正确放置并移至前面
plt.title('书籍评分分布')
plt.xlabel('评分')
plt.ylabel('数量')
plt.show()

# 出版社计数
counts = df['出版社'].value_counts()
top_publishers = counts[:10]
for author, count in counts.items():
    print(f"出版社：{author}，出现次数：{count}")


# 出版社最多的出版社
plt.figure(figsize=(10, 6))
colors = sns.color_palette('viridis', len(top_publishers))  # 获取与数据长度相匹配的颜色序列
for i, (publisher, value) in enumerate(top_publishers.items()):
    sns.barplot(x=[publisher], y=[value], color=colors[i], label=publisher if i == 0 else None)  # 第一个标签保留，其余隐藏
plt.legend(title='出版社')  # 显示图例，但仅有一个出版社名称作为示例
plt.xticks(rotation=45)
plt.title('出版社书籍数排名')
plt.ylabel('书籍数')
plt.show()

# 作者计数
author_counts = df['作者'].value_counts()
top_authors = author_counts[:10]
for author, count in author_counts.items():
    print(f"作者：{author}，出现次数：{count}")

# 作者多的书籍
plt.figure(figsize=(10, 6))
colors = sns.color_palette('plasma', len(top_authors))  # 同上，获取plasma调色板
for i, (author, value) in enumerate(top_authors.items()):
    sns.barplot(x=[author], y=[value], color=colors[i], label=author if i == 0 else None)
plt.legend(title='作者')  # 显示图例标题，但只有第一个作者名称
plt.xticks(rotation=45)
plt.title('作者书籍数排名')
plt.ylabel('书籍数')
plt.show()