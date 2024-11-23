# AutoStack

基于大语言模型的全栈项目自动生成工具

## NestJS后端生成
- 执行：npm install，安装依赖文件
- .env文件下需要配置数据库地址、用户名、密码等信息
- 后端代码生成后，需要执行以下代码初始化数据库
```bash
npx prisma migrate dev --name init
```
- 执行：npm run start启动项目