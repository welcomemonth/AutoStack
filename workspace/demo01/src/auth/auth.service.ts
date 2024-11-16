import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UserService } from '../user/user.service';
import { CreateUserDto } from 'src/user/dto/create-user.dto';
import { PasswordService } from './password.service';

@Injectable()
export class AuthService {
  constructor(
    private userService: UserService,
    private jwtService: JwtService,
    private passwordService: PasswordService,
  ) {}

  async signIn(username: string, pass: string) {
    const user = await this.userService.findOneByName(username);
    const isPasswordValid = await this.passwordService.comparePassword(pass, user?.password);

    if (!isPasswordValid) {
      throw new UnauthorizedException("Invalid credentials");
    }
    const payload = { username: user.username, sub: user.id };

    return {
      token: await this.jwtService.signAsync(payload),
    };
  }

  async signUp(signUpDto: CreateUserDto) {
    signUpDto.password =await this.passwordService.hashPassword(signUpDto.password);
    let newUser = await this.userService.create(signUpDto);
    const payload = { username: newUser.username, sub: newUser.id };
    return {
        access_token: await this.jwtService.signAsync(payload),
    };
  }

}