# 使用官方的Node.js 18基础镜像
FROM node:18

# 设置工作目录
WORKDIR /app

# 全局安装NestJS CLI
RUN npm install -g @nestjs/cli

# 安装 PostgreSQL 客户端
RUN apt-get update && apt-get install -y postgresql postgresql-client

# 设置环境变量
ENV DATABASE_HOST=localhost \
    DATABASE_PORT=5432 \
    DATABASE_USER=postgres \
    DATABASE_PASSWORD=postgres \
    DATABASE_NAME=postgres
# 暴露一个默认的开发端口（可选）
EXPOSE 3000
# 启动脚本
CMD ["sh", "/app/docker-entrypoint.sh"]
# 由于这是一个环境搭建镜像，所以不需要指定CMD
