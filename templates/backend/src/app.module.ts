import { Module } from '@nestjs/common';
import { UserModule } from './user/user.module';
import { AuthModule } from './auth/auth.module';
import { PrismaModule } from './prisma/prisma.module';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    UserModule,
    AuthModule,
    PrismaModule,
  ],
  exports: [],
  providers:[AppService],
  controllers: [ AppController ]
})
export class AppModule {}
