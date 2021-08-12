# use

```

# 设置环境变量，或修改代码
api_base=xxx ding_token=xxx

# 发送钉钉文章记录，每天早上3点获取，9点发送
0 3,9 * * * python3 client/send.py
```
