import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 城市和职位映射字典
city_mapping = {'bj': "北京", 'sh': "上海", 'qz': "广州", 'SZ': "深圳", 'cq': "重庆", 'km': '昆明', 'hz': '杭州'}
job_mapping = {'fuwuy': '服务业', 'shengchanzhz': '生产制造', 'nchuanmei': '传媒/影视/直播', 'nsheji': '设计',
               'jinrongmy': '金融贸易'}

# 按城市存储数据的字典
city_data = {city_name: [] for city_name in city_mapping.values()}

# 请求头配置
cookies = {
    "xxzlxxid": "pfmxa5lFVaImqpTMwTwFLXvZRhtz9xTl42sIL3SAIZ7RbDhBP8yf7NBcCR6kFs4ACgHD",
    "id58": "CroOxGcl1yAZv+y9CiotAg==",
    "xxzlclientid": "8a8ccbc0-60de-409e-a9ff-1730533153034",
    "58tj_uuid": "e2fecfea-c1e6-4754-b85d-db9dab3b2f25",
    "als": "0",
    "wmda_uuid": "39bafce57ff3203c0cca639a57f54bd2",
    "wmda_new_uuid": "1",
    "ppStore_fingerprint": "D8C1CE3E8C671993AF75EEC14DB91951974A9D453AF888DF%EF%BC%BF1730535631244",
    "Hm_lvt_b4a22b2e0b326c2da73c447b956d6746": "1742694991",
    "myfeet_tooltip": "end",
    "58uname": "is2vljdc9",
    "passportAccount": "atype=0&bstate=0",
    "param8616": "1",
    "param8716kop": "1",
    "wmda_visited_projects": "%3B2385390625025%3B1731916484865%3B29317198571852",
    "fzq_h": "c38645556b7c8385395991f5e07972df_1742789592033_c71be38313984016b44a2362ae18565f_1928886929",
    "city": "bj",
    "commontopbar_new_city_info": "1%7C%E5%8C%97%E4%BA%AC%7Cbj",
    "58home": "bj",
    "commontopbar_ipcity": "bj%7C%E5%8C%97%E4%BA%AC%7C0",
    "f": "n",
    "sessionid": "61d50cb5-8f00-4321-9b0b-3728efb3dc51",
    "Hm_lvt_5bcc464efd3454091cf2095d3515ea05": "1742695027,1742790132,1742792406",
    "HMACCOUNT": "D18D2CDB0E6B4206",
    "userid360_xml": "13ED160DE21D9A4A44D9BBD98F12A917",
    "time_create": "1745392621105",
    "jobBottomBar": "1",
    "www58com": "\"AutoLogin=false&UserID=0&UserName=&CityID=1&Email=&AllMsgTotal=0&CommentReadTotal=0&CommentUnReadTotal=0&MsgReadTotal=0&MsgUnReadTotal=0&RequireFriendReadTotal=0&RequireFriendUnReadTotal=0&SystemReadTotal=0&SystemUnReadTotal=0&UserCredit=1&UserScore=0&PurviewID=&IsAgency=false&Agencys=null&SiteKey=53115061EEDA8F62C68B743FD521F8CF9&Phone=&WltUrl=&UserLoginVer=null&LT=1742804884831\"",
    "fzq_js_zhaopin_list_pc": "370763bfb6e2fc141bf3b3f36d7937ed_1742809261330_6",
    "Hm_lpvt_5bcc464efd3454091cf2095d3515ea05": "1742809261",
    "wmda_report_times": "1",
    "PPU": "\"UID=85456455226406&UN=is2vljdc9&TT=580d4b348c4aab90b93746a92f059552&PBODY=hoaG44EBkJPsVTs6BibYxohaF3LxNzdtVLlX3LfTpxvNtlDHk1pgNoavSv5naCpRcGxVTO320L3b2GBvYmobpeMMmzbTUHGc8JgL7KZl-HPDjNttCssqIAU0HUqHiLvg39YuIqykUzLn1tk7n7YaaJPjp9ZQzQqW5lG4SeJeqG4&VER=1&CUID=u28AqpReYfSQV5mwd169fw\"",
    "xxzlbbid": "pfmbM3wxMDI3M3wxLjEwLjF8MTc0MjgxMzc5MjQyMjcyODE0MHxkakd3cGQzak9WTVVLT1NZeGhVd2srZ1FzMXo3cmRDMnlZOWlzR3gvU09JPXw1YTU2N2FiY2FhMjVkMzAzNDdiYWU5MjMyMjUwZjRhMF8xNzQyODEzNzkyNDYzX2Y5NmE2M2RmZWJlNDQxOWNhNmYxYmYyN2M3MGEzYTY0XzE5Mjg4ODY5Mjl8OTllYzgzMjg0ZmE1NjYzNjY0OWIzZTYyM2U3MmM2ODVfMTc0MjgxMzc5MjAxMF8yNTQ=",
    "JSESSIONID": "56FC8A729D20434C918D47BF46117073",
    "new_session": "1",
    "new_uv": "12",
    "utm_source": "",
    "spm": "",
    "init_refer": "https%253A%252F%252Fcallback.58.com%252F",
    "wmda_session_id_1731916484865": "1742813792985-d8419777-79a6-4402-8d1f-541a586ec01a"
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
}


def get_page_data(city_code, job_code, page):
    """获取单页数据"""
    url = f"https://{city_code}.58.com/{job_code}/pn{page}/?PGTID=0d000000-0000-0cbd-56a6-5d5960a03580&ClickID=1"
    try:
        time.sleep(random.uniform(1, 2))
        response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return None


def parse_page(html, city_name, job_name):
    """解析页面数据"""
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', {'id': 'list_con'})
    if not ul:
        return []

    page_data = []
    for li in ul.find_all('li', class_='job_item'):
        job_info = {
            '城市': city_name,
            '职位类型': job_name,
            '职位名称': li.find('span', class_='name').text.strip() if li.find('span', class_='name') else '未知',
            '薪资': li.find('p', class_='job_salary').text.strip() if li.find('p', class_='job_salary') else '未知',
            '学历要求': '未知',
            '工作经验': '未知',
            '公司名称': '未知'
        }

        if require := li.find('p', class_='job_require'):
            spans = require.find_all('span')
            if len(spans) >= 3:
                job_info.update({
                    '学历要求': spans[1].text.strip(),
                    '工作经验': spans[2].text.strip()
                })

        if company := li.find('div', class_='comp_name'):
            if company_link := company.find('a'):
                job_info['公司名称'] = company_link.text.strip()

        page_data.append(job_info)

    return page_data


def has_next_page(soup):
    """检查是否存在下一页"""
    next_btn = soup.find('a', class_='next')
    return next_btn and 'disable' not in next_btn.get('class', [])


def scrape_job(city_code, city_name, job_code, job_name):
    """采集单个职位的所有页面"""
    page = 1
    max_pages = 10

    while page <= max_pages:
        print(f"正在采集 {city_name}-{job_name} 第{page}页")

        if html := get_page_data(city_code, job_code, page):
            soup = BeautifulSoup(html, 'html.parser')
            page_data = parse_page(html, city_name, job_name)

            if not page_data:
                print(f"第{page}页无数据，终止采集")
                break

            city_data[city_name].extend(page_data)
            print(f"已采集 {len(page_data)} 条数据")

            if not has_next_page(soup):
                break
            page += 1
        else:
            print("获取页面失败，终止采集")
            break


def save_to_excel():
    """按城市保存到不同工作表"""
    with pd.ExcelWriter('58同城招聘数据（3）.xlsx', engine='openpyxl') as writer:
        for city_name, data in city_data.items():
            if data:
                df = pd.DataFrame(data)
                df = df.drop_duplicates()
                sheet_name = city_name[:10] if len(city_name) > 10 else city_name
                df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False,
                    columns=['城市', '职位类型', '职位名称', '薪资', '学历要求', '工作经验', '公司名称']
                )
                print(f"{city_name} 已保存 {len(df)} 条数据")


# 主采集流程
for city_code, city_name in city_mapping.items():
    print(f"\n{'=' * 30} 开始采集 {city_name} {'=' * 30}")

    for job_code, job_name in job_mapping.items():
        print(f"当前职位：{job_name}")
        scrape_job(city_code, city_name, job_code, job_name)
        time.sleep(random.uniform(5, 10))

    print(f"{city_name} 采集完成！")
    time.sleep(random.uniform(15, 25))

# 保存数据
if any(len(data) > 0 for data in city_data.values()):
    save_to_excel()
    print("\n所有城市数据已保存！")
else:
    print("未采集到任何数据")


