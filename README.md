# AutoStack

基于大语言模型的全栈项目自动生成工具

## NestJS后端生成
- .env文件下需要配置数据库地址、用户名、密码等信息
- 后端代码生成后，需要执行以下代码初始化数据库
```bash
npx prisma migrate dev --name init
```