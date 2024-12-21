from pathlib import Path
from typing import Union


class PathUtil:
    @staticmethod
    def switch_linux_to_windows(win_path: Union[str, Path], linux_path: Union[str, Path], replace_path: str):
        """
        将写入容器的路径替换为写入windows的路径，
        例如 win_path = C:\\aaa\bbb
            linux_path = /app/ccc/ddd
            repalce_path = '/app'
            则返回值：C:\\aaa\\bbb\\ccc\\ddd
        :param win_path:
        :param linux_path:
        :param replace_path:
        :return:
        """
        win_path = Path(win_path)
        linux_path = Path(linux_path)

        # 替换路径
        new_path = win_path / linux_path.relative_to(replace_path)
        return new_path


