export class User {
  id: string;

  username: string;

  password: string;

  role: RoleLevel;
}

export enum RoleLevel {
  ADMIN = "ADMIN", // 最高权限
  USER = "USER",
}


