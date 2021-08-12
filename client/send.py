import requests
import logging
import os
import datetime
import json

os.environ.setdefault('api_base', 'http://xxxx')
os.environ.setdefault('ding_token', 'xxxx')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

yesterday = datetime.date.today() + datetime.timedelta(-2)
json_path = '%s.json' % yesterday
data_url = "%s/weibo/%s?type=json" %(os.environ.get("api_base"), yesterday)
ding_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % os.environ.get("ding_token")

logger.info('json_path: ' + json_path)
logger.info('ding_url: ' + ding_url)
logger.info('data_url: ' + data_url)


def get_data():
    """获取数据 & 写入json"""
    logger.info('开始获取数据')
    response = requests.get(data_url)

    if response.status_code != 200:
        logger.error('Sever error, check ' + data_url)
        return

    logger.info('获取数据完成')
    response_json_data = response.json()

    if response_json_data is None:
        logger.info('Response data is none, exit')
        return

    logger.info('开始写入数据')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(response_json_data, f, indent=2)
        logger.info('写入文件完成')


def sub_data():
    """发布叮叮"""
    logger.info('开始发送到dingtalk')
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    response = requests.post(url=ding_url, data=json.dumps(
        # {
        #     "feedCard": {
        #         "links": format_to_feed_card(data=json_data)
        #     },
        #     "msgtype": "feedCard"
        # }
        {
            "msgtype": "markdown",
            "markdown": {
                "title": "今日文章列表",
                "text": format_to_markdonw(json_data)

            },
        }

    ), headers={
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    })

    if response.status_code == 200 and response.json()['errcode'] == 0:
        logger.info('发送成功')
    else:
        logger.error('发送失败: %s' % response.text)


def format_to_feed_card(data):
    """这个模式好看，但是链接没法复制"""
    result = []
    for item in data:
        result.append({
            "title": item['text'].replace('网页链接', ''),
            "messageURL": item['text_link'].split(',')[0],
            "picURL": item['pics'].split(',')[0]
        })
    result.append({
        "title": "作业帮内部导航页",
        "messageURL": "http://ued.zuoyebang.cc/documents/",
        "picURL": "https://www.flaticon.com/premium-icon/icons/svg/520/520464.svg"
    })
    return result


def format_to_markdonw(data):
    """这个模式不好看"""
    result = []
    for item in data:
        result.append(
            "- [%s](%s) %s" % (get_text_with_md(item), item['text_link'].split(',')[0], get_pic_with_md(item)))

    return ("\n").join(result)


def get_text_with_md(item):
    arr = item['text'].split('网页链接')
    if arr[1].strip():
        return arr[1]
    else:
        return arr[0]


def get_pic_with_md(item):
    return ""
    pic = item['pics'].split(',')[0]
    if pic:
        return "![](%s)" % pic
    else:
        return ""


if __name__ == '__main__':
    if os.path.exists(json_path):
        sub_data()
    else:
        get_data()

