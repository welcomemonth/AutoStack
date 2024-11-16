import { Module } from '@nestjs/common';
import { UserModule } from './user/user.module';
import { AuthModule } from './auth/auth.module';
import { PrismaModule } from './prisma/prisma.module';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { EntityModule } from './${entity_lower_underline}/$${entity_lower_underline}.module';

@Module({
  imports: [
    UserModule,
    AuthModule,
    PrismaModule,
    EntityModule
  ],
  exports: [],
  providers:[AppService],
  controllers: [ AppController ]
})
export class AppModule {}
