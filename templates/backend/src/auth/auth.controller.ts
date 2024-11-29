import {
    Body,
    Controller,
    Get,
    Post,
    Request,
    HttpCode,
    HttpStatus,
    UseGuards,
} from '@nestjs/common';
import { AuthService } from './auth.service';
import { CreateUserDto } from 'src/user/dto/create-user.dto';
import { SignInDto } from './dto/signin.dto';
import { Role } from './decorators/role.decorator';
import { RoleLevel } from '@prisma/client';
import { AuthGuard } from './auth.guard';

@Controller("auth")
export class AuthController {
    constructor(private readonly authService: AuthService) {}

    @Post('login')
    signIn(@Body() signInDto: SignInDto) {
      return this.authService.signIn(signInDto.username, signInDto.password);
    }

    @UseGuards(AuthGuard)
    @Get('profile')
    getProfile(@Request() req) {
      return req.user;
    }

    @Post('register')
    signUp(@Body() signUpDto: CreateUserDto) {
      return this.authService.signUp(signUpDto);
    }

    @Role(RoleLevel.ADMIN)
    @UseGuards(AuthGuard)
    @Get('admin')
    getAdmin() {
      return 'Admin page';
    }

}
