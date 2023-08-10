import requests
import json

class WxPushClient:

    def __init__(self):
        self.url = 'https://wxpusher.zjiecode.com/api/send/message'
    
    def push(self, summary, content, topics):
        headers = {
            'Content-Type': 'application/json'
        }
        params = {
            'appToken': 'AT_RG34cndHOzAUVMi8zzqjRBPVaBfBZSM7',
            'content': content,
            'summary': summary,
            'contentType': 1,
            'topicIds': topics,
            'url': '',
            'verifyPay': 'false'
        }
        
        try:
            resp = requests.post(self.url, headers=headers, data=json.dumps(params))
            resp_data = resp.json()
            print(resp_data)
            if resp_data['code'] != 1000:
                print("微信推送失败, params: ", params, ", err: ", resp_data)
        except Exception as err:
            print("微信推送失败, 抛出异常, params: ", params, ", err: ", err)


if __name__ == '__main__':
    wx_push_client = WxPushClient()
    wx_push_client.push('test', 'test')