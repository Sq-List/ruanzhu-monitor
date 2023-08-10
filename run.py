import requests
from wx_push import WxPushClient
from retry import retry

@retry(10)
def exec():
    url = "https://gateway.ccopyright.com.cn/registerQuerySoftServer/userCenter/flowNumberHistory/495622356396584960/2023R11L1375707"

    headers = {
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        'Authorization': "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJpc3MiOiJ1TDVBTDlMUkp1M291cVdqbThYSmdacXo0Q3hNY3VJVyJ9.hCgWmJ9hDy4l1ejfR9g0rvvtkbyg8GOtg-TESkdFfXc",
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
        'authorization_key': "uL5AL9LRJu3ouqWjm8XJgZqz4CxMcuIW",
        'authorization_token': "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJpc3MiOiJ1TDVBTDlMUkp1M291cVdqbThYSmdacXo0Q3hNY3VJVyJ9.hCgWmJ9hDy4l1ejfR9g0rvvtkbyg8GOtg-TESkdFfXc",
        'device': "pc",
        'sec-ch-ua': "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"macOS\"",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers)

    wx_push_client = WxPushClient()
    if response.status_code == 200:
        data = response.json()
        state = []
        for node in data['data']:
            state.append(node['userStatus'])
        wx_push_client.push("软著状态变更", "状态变更："+",".join(state), [11144])

    elif response.status_code == 403:
        wx_push_client.push("软著登录过期", "登录状态过期，需重新登录，更新token", [11144])
    elif response.status_code == 502:
        raise Exception("返回502，重试")

    # print(response.status_code)
    # print(response.json())



if __name__ == '__main__':
    exec()