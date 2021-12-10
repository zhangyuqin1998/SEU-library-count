from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

URL= "http://www.lib.seu.edu.cn/lib.php"
 #构建请求头
header = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Host': 'www.lib.seu.edu.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4507.400'}

TIME_INTERVAL = 5 * 60
HOURS = 24
if __name__ == "__main__":
    response = requests.get(URL, headers=header) #获取响应
    flag = response.status_code #响应码
    print(f"响应码为：{flag}")
    soup = BeautifulSoup(response.content, "lxml")  # 用lxml解析器解析该网页的内容

    # print(response.content.decode())  #返回字节信息
    # print(response.text)  #返回文本内容
    # print(soup)
    localtime = []
    lib_cnt_jiulonghu = []
    lib_cnt_sipailou = []
    lib_cnt_dingjiaqiao = []

    f = 0
    while flag == 200 and f <= (HOURS * 60 * 60/ TIME_INTERVAL):
        response = requests.get(URL, headers=header) #获取响应
        flag = response.status_code
        soup = BeautifulSoup(response.content, "lxml")  # 用lxml解析器解析该网页的内容

        localtime_ = time.asctime(time.localtime(time.time())) #读取当前时间
        localtime.append(localtime_)

        lib_cnt = soup.find_all('span')
        lib_cnt_jiulonghu.append(lib_cnt[0].string)
        lib_cnt_sipailou.append(lib_cnt[1].string)
        lib_cnt_dingjiaqiao.append(lib_cnt[2].string)
        print(f'当前时间为{localtime_}，九龙湖{lib_cnt[0].string}，四牌楼{lib_cnt[1].string}，丁家桥{lib_cnt[2].string}')
        time.sleep(TIME_INTERVAL)
        f += 1

    df = pd.DataFrame([localtime, lib_cnt_jiulonghu, lib_cnt_sipailou, lib_cnt_dingjiaqiao],
                      columns=["时间","九龙湖在馆人数","四牌楼在馆人数","丁家桥在馆人数"])

    df.to_csv("SEU_LIB_CNT.csv", mode="w")
    print("Done!")
