import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

# 邮件发送配置
sender_email = "386857251@qq.com"  # 替换为你的 QQ 邮箱地址
sender_password = "qosozmmhfzyybhgi"  # 替换为你的 QQ 授权码（应用专用密码）
recipient_email = "zhengxinlilili@gmail.com"  # 替换为接收方的 Gmail 邮箱

# 定义需要爬取的网址和对应的主题
urls = [
    ("https://tophub.today/n/WnBe01o371", "微信热榜数据"),
    ("https://tophub.today/n/NKGoRAzel6", "吾爱破解热榜数据"),
    ("https://tophub.today/n/Q1Vd5Ko85R", "36K数据"),
    ("https://tophub.today/n/Y2KeDGQdNP", "少数派数据"),
    ("https://tophub.today/n/WYKd6jdaPj", "豆瓣小组数据")
]

# 遍历每个网址和对应的主题
for url, subject in urls:
    # 初始化邮件内容
    email_content = ""

    # 发送请求并检查是否成功
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析 HTML 页面
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找包含热点数据的 table 标签
        table = soup.find('table', class_='table')
        
        if table:
            hotspots = []

            # 获取所有的行
            rows = table.find_all('tr')

            for row in rows:
                # 获取每一行的各个列
                cols = row.find_all('td')
                
                # 确保这一行有足够的列数
                if len(cols) >= 3:
                    # 提取标题（第二列）、链接和访问量（第三列）
                    title_tag = cols[1].find('a')
                    if title_tag:
                        title = title_tag.get_text(strip=True)  # 获取标题文本
                        link = title_tag['href']  # 获取链接

                        # 获取访问量（第三列）
                        views = cols[2].get_text(strip=True)

                        # 保存提取的信息
                        hotspots.append({
                            'title': title,
                            'link': link,
                            'views': views
                        })
            
            # 输出爬取到的数据
            if hotspots:
                email_content = f"以下是爬取到的{subject}数据：\n\n"
                for idx, hotspot in enumerate(hotspots, 1):
                    email_content += f"热点 {idx}:\n"
                    email_content += f"标题: {hotspot['title']}\n"
                    email_content += f"链接: {hotspot['link']}\n"
                    email_content += f"访问量: {hotspot['views']}\n"
                    email_content += '-' * 40 + '\n'
            else:
                email_content = f"没有找到任何{subject}热点信息"
        else:
            email_content = f"未找到{subject}目标表格"
    else:
        email_content = f"请求失败，状态码: {response.status_code}"

    # 创建邮件对象
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = f"{subject}"

    # 附加文本内容
    message.attach(MIMEText(email_content, "plain", "utf-8"))

    try:
        # 连接到 QQ 的 SMTP 服务器
        with smtplib.SMTP("smtp.qq.com", 587) as server:
            server.starttls()  # 启用加密传输
            server.login(sender_email, sender_password)  # 登录
            server.sendmail(sender_email, recipient_email, message.as_string())  # 发送邮件

        print(f"邮件发送成功！({subject})")
    except Exception as e:
        print(f"邮件发送失败: {e}")
