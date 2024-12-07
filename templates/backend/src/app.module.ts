import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    PrismaModule,
  ],
  exports: [],
  providers:[AppService],
  controllers: [ AppController ]
})
export class AppModule {}
