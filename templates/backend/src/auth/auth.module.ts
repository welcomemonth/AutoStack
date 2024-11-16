import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { UserModule } from 'src/user/user.module';
import { UserService } from 'src/user/user.service';
import { AuthController } from './auth.controller';
import { JwtModule } from '@nestjs/jwt';
import { jwtConstants } from './constants';
import { PrismaModule } from 'src/prisma/prisma.module';
import { PasswordService } from './password.service';

@Module({
  imports: [
    UserModule,
    PrismaModule,
    JwtModule.register({
      global: true,
      secret: jwtConstants.secret,
      signOptions: { expiresIn: '1200s' },
    }),
  ],
  providers: [AuthService, UserService, PasswordService],
  exports: [AuthService],
  controllers: [AuthController]
})
export class AuthModule {}
