import requests
import sys
from datetime import datetime 

from ruan_zhu_exception import RuanZhuExceptin
from wx_push import WxPushClient
from retry import retry

@retry(10)
def exec(key, token):
    print("key: ", key, ", token: ", token)
    url = "https://gateway.ccopyright.com.cn/registerQuerySoftServer/userCenter/flowNumberHistory/495622356396584960/2023R11L1375707"

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        'Authorization': "Bearer " + token,
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
        'Host': "gateway.ccopyright.com.cn",
        'Origin': "https://register.ccopyright.com.cn",
        'Pragma': "no-cache",
        'Referer': "https://register.ccopyright.com.cn/accountDetails.html?flowNumber=2023R11L1375707&current=soft_register&time=1691487539112",
        'Sec-Fetch-Dest': "empty",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Site': "same-site",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        'authorization_key': key,
        'authorization_token': token,
        'device': "pc",
        'sec-ch-ua': "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"macOS\"",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, timeout=10)

    wx_push_client = WxPushClient()
    if response.status_code == 200:
        try:
            data = response.json()
            state = []
            for node in data['data']:
                state.append(node['userStatus'])

            create_time = data['data'][-1]['createTime']
            # print(create_time)

            last_update_time = datetime.fromtimestamp(create_time / 1000)
            now = datetime.now()

            # print((now - last_update_time))
            diff = (now - last_update_time).total_seconds() / 60
            print("diff: ", diff)
            if diff < 30:
                wx_push_client.push("软著状态变更", "状态："+",".join(state), [11144])
            elif now.hour == 8 and now.min <= 20:
                wx_push_client.push("每日软著状态提醒", "状态："+",".join(state), [11144])
        except Exception as e:
            print(str(e))
            wx_push_client.push("软著监控代码出错", str(e), [11144])

    elif response.status_code == 403:
        wx_push_client.push("软著登录过期", "登录状态过期，需重新登录，更新token", [11144])
    elif response.status_code == 502:
        raise RuanZhuExceptin("返回502，重试")

    # print(response.status_code)
    # print(response.json())



if __name__ == '__main__':
    exec(sys.argv[1], sys.argv[2])
