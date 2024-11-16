import { SetMetadata } from '@nestjs/common';
import { RoleLevel } from '@prisma/client';

export const Role = (roleLevel: RoleLevel) => SetMetadata('roleLevel', roleLevel);
