fork: [https://github.com/dataabc/weibo-crawler](https://github.com/dataabc/weibo-crawler)

# install 
```bash
pip install -r requirements.txt
python weibo.py
```

# server
```bash
go install
go build
./main &
```

# 开机启动

- 按下win+R调出运行窗口，并输入“shell:startup”即可进入开机启动文件夹，托入weibo.bat
- 按下win+R调出运行窗口，并输入“gpedit.msc”，windows配置，双击启动，选择weibo.bat