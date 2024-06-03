# BackEnd/Dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目的需求文件，并安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到容器中
COPY . .

# 添加调试
RUN ls -la /app
RUN cat /app/app.py

# 暴露应用运行的端口
EXPOSE 5050

# 设置默认启动命令
CMD ["python", "app.py"]
