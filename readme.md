### 代码相关问题

1. 生产requirements.txt文件：`pip freeze > requirements.txt`

2. 后端统一返回格式:

   ```json
   {
     "success": true,
     "message": "成功",
     "data": {}
   }
   ```

3. 待解决的问题：
   1. ~~解决函数内部的db引入：`from app import db  # 避免循环导入`~~

### Ubuntu云服务器运行方法：

**安装Anconda3：**

```bash
# 安装Anconda3
sudo apt update && sudo apt install wget -y # 安装wget
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh # 下载脚本
chmod +x Anaconda3-2024.06-1-Linux-x86_64.sh # 给脚本赋权
./Anaconda3-2024.06-1-Linux-x86_64.sh  # 运行脚本，注意：阅读完隐私协议后，有个输入安装位置的提示，请直接Enter即可。最后`conda init --reverse $SHELL`? [yes|no]的选项，选择yes以便添加path环境
source ~/.bashrc  # 是重新加载当前用户的 .bashrc 文件,使path环境生效
conda create -n python11 python=3.11  # 安装python虚拟环境，后面的提示选y。
conda activate python11  # 激活环境
```

**部署Flask：**

1. 准备Flask程序，并生成`requirements.txt`文件

2. 去防火墙开放5000端口

3. 将本地的Flask应用上传到云服务器的某文件夹下

   修改`app.py`启动配置，绑定**内网**IP：`app.run(host="xxx.xx.xx.xxx", port=5000, debug=False)`

4. cd到文件夹内

5. 安装requirements.txt： `pip install -r requirements.txt`
      ```bash
      # Ubuntu可能出现报错：pkg-config: not found
      sudo apt update
      sudo apt install pkg-config # 安装pkg-config
      # 如果是MySQL数据库
      sudo apt install libmysqlclient-dev
      # 如果是MariaDB数据库
      # sudo apt install libmariadb-dev
      pip install -r requirements.txt
      ```

6. 最后运行：`python app.py`

      需要注意的是：**Flask程序需要允许CORS**

      ```python
      from flask_cors import CORS
      # 初始化 Flask 应用
      app = Flask(__name__)
      # 启用 CORS 允许跨域请求
      CORS(app, supports_credentials=True)
      ```

**高并发运行**

1. 安装gunicorn：`pip install gunicorn`
  
2. 编写 `gunicorn.conf`文件，与 `app.py`存放在同一目录，并在该目录中创建log相关文件，内容如下：
  
   ```ini
   # gunicorn.conf
   
   bind = "0.0.0.0:5000"  # 监听所有网络接口，端口为5000
   workers = 4  # 启动四个工作进程，适合高并发
   backlog = 2048  # 设置等待连接的最大请求数量
   pidfile = "log/gunicorn.pid"  # 指定 Gunicorn 的进程ID文件路径
   accesslog = "log/access.log"  # 记录访问日志的文件路径
   errorlog = "log/debug.log"  # 记录错误日志的文件路径。
   timeout = 600 # 设置请求超时时间为 600 秒。
   debug=False  # 设置为 False，表示不启用调试模式
   capture_output = True  # 捕获标准输出和错误输出，并将其写入日志文件
   ```
   
3. 并在`app.py`同级目录下，创建`log/access.log`和`log/debug.log`文件
   4. 运行代码：`gunicorn --config gunicorn.conf app:app`
   

**使用域名访问**

详细请查看：https://romcere.top/archives/flask#%E4%BD%BF%E7%94%A8%E5%9F%9F%E5%90%8D%E8%AE%BF%E9%97%AEapi-Nginx%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86

**后台运行-systemd守护进程**

1. 创建一个 `gunicorn.service`服务文件，放在 `/etc/systemd/system`下，内容如下（需要根据实际情况修改文件位置）：
  
   ```ini
   [Unit]
   Description=Gunicorn instance to serve your app
   After=network.target
   
   [Service]
   User=ubuntu
   Group=ubuntu
   WorkingDirectory=/home/ubuntu/PunchInBackstage
   Environment="PATH=/home/ubuntu/anaconda/envs/python11/bin"
   ExecStart=/home/ubuntu/anaconda/envs/python11/bin/gunicorn --config /home/ubuntu/PunchInBackstage/gunicorn.conf app:app
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   `User`：用户名，如果是CentOS，则改为`root`
   
   `Group`：用户组，如果是CentOS，则改为`root`
   
   `WorkingDirectory`：工作目录，只到后端文件的目录即可
   
   `Environment`：python程序
   
   `ExecStart`：这里为gunicorn运行命令，需更换前者文件位置
   
2. 启用并启动 Gunicorn 服务：
  
   ```bash
   sudo systemctl enable gunicorn  # 设置系统启动时自动启动，
   sudo reboot  # 重启服务器
   sudo systemctl status gunicorn  # 查看gunicorn状态，检查是否启动
   # 如果修改了gunicorn.service文件，需重载并重启gunicorn服务
   sudo systemctl daemon-reload  # 重载配置文件
   sudo systemctl restart gunicorn  # 重启gunicorn服务
   ------------------------------------------------------------其他命令
   sudo systemctl start gunicorn  # 启动gunicorn服务
   sudo systemctl stop gunicorn  # 停止gunicorn服务
   ```
   

**其他问题**

1. 当需要为`python`添加包/依赖时：
  
   ```bash
   conda activate python11 # 先激活环境
   pip install xxx  # 再安装
   sudo systemctl restart gunicorn  # 重启gunicorn服务
   sudo systemctl status gunicorn  # 查看gunicorn状态
   ```
   



