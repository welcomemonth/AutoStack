import { Injectable } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { PrismaService } from 'src/prisma/prisma.service';
import { UpdateUserInput } from './dto/update-user.dto';
import { User } from '@prisma/client';

@Injectable()
export class UserService {
  constructor(
    private readonly prisma: PrismaService
  ) {}

  create(
    createUserDto: CreateUserDto
  ): Promise<User> {
    return this.prisma.user.create({
      data: {
        password: createUserDto.password,
        username: createUserDto.username,
        role: createUserDto.roleLevel,
      },
    })
  }

  findAll(): Promise<User[]> {
    return this.prisma.user.findMany();
  }

  findOne(id: string): Promise<User> {
    return this.prisma.user.findUnique({
      where: { id: id },
    });
  }

  findOneByName(username: string): Promise<User> {
    return this.prisma.user.findFirst({
      where: { username: username },
    });
  }

  async update(id: string, updateChatInput: UpdateUserInput) {
    return this.prisma.user.update({
      where: { id: id },
      data: updateChatInput,
    });
  }

  async remove(id: string) {
    return this.prisma.user.delete({
      where: { id: id },
    });
  }

}
