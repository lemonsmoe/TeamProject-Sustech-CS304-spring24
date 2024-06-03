# vue/Dockerfile
FROM node:14

# 设置工作目录
WORKDIR /app

# 复制项目的package.json，并安装Node.js依赖
COPY package*.json ./
RUN npm install

# 复制项目文件到容器中
COPY . .

# 构建项目
RUN npm run build

# 使用Nginx来服务构建后的文件
FROM nginx:latest
COPY --from=0 /app/dist /usr/share/nginx/html

# 暴露Nginx运行的端口
EXPOSE 80

# 设置默认启动命令
CMD ["nginx", "-g", "daemon off;"]

