import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
    // 配置 Swagger 文档
  const config = new DocumentBuilder().build();
  // 创建 Swagger 文档
  const document = SwaggerModule.createDocument(app, config);
  // 启用 Swagger UI
  SwaggerModule.setup('docs', app, document);

  app.useGlobalPipes(new ValidationPipe());
  await app.listen(3000);
}
bootstrap();
