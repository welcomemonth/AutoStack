import { IsString, IsOptional, IsArray, IsNumber } from 'class-validator';
import { RoleLevel } from '@prisma/client';


export class UpdateUserDto{
    @IsOptional()
    @IsString()
    username?: string;
  
    @IsOptional()
    @IsString()
    password?: string;

    @IsOptional()
    roleLevel?: RoleLevel;
}

export interface UpdateUserInput{
    username?: string;
    password?: string;
    roleLevel?: RoleLevel;
}