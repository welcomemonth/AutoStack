import json
import unittest
import os
import json
import shutil
from pathlib import Path
from autostack.utils import FileUtil  # 假设 FileUtil 存放在 file_util.py 文件中


class TestFileUtil(unittest.TestCase):

    def setUp(self):
        """在每个测试用例之前运行，创建一些测试所需的临时目录和文件"""
        self.test_dir = Path("test_dir")
        self.test_file = self.test_dir / "test_file.txt"
        self.test_append_file = self.test_dir / "test_append_file.txt"
        self.test_env_file = self.test_dir / "test.env"

        if not self.test_dir.exists():
            os.makedirs(self.test_dir)

    def tearDown(self):
        """在每个测试用例后运行，清理文件系统"""
        if self.test_file.exists():
            os.remove(self.test_file)
        if self.test_append_file.exists():
            os.remove(self.test_append_file)
        if self.test_env_file.exists():
            os.remove(self.test_env_file)
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_create_dir(self):
        """测试 create_dir 方法是否创建目录"""
        dir_path = self.test_dir / "new_dir"
        FileUtil.create_dir(dir_path)
        self.assertTrue(dir_path.exists())

    def test_write_file(self):
        """测试 write_file 方法是否能够正确写入文件"""
        FileUtil.write_file(self.test_file, "Hello, World!")
        with open(self.test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!")

    def test_append_file(self):
        """测试 append_file 方法是否能够正确追加内容"""
        FileUtil.write_file(self.test_append_file, "Hello")
        FileUtil.append_file(self.test_append_file, ", World!")
        with open(self.test_append_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "Hello, World!")

    def test_remove_file(self):
        """测试 remove_file 方法是否能够删除文件"""
        FileUtil.write_file(self.test_file, "Delete Me!")
        FileUtil.remove_file(self.test_file)
        self.assertFalse(self.test_file.exists())

    def test_remove_dir(self):
        """测试 remove_dir 方法是否能够删除目录"""
        FileUtil.create_dir(self.test_file)
        FileUtil.remove_dir(self.test_dir)
        self.assertFalse(self.test_dir.exists())

    def test_clear_file(self):
        """测试 clear_file 方法是否能够清空文件内容"""
        FileUtil.write_file(self.test_file, "Some content")
        FileUtil.clear_file(self.test_file)
        with open(self.test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "")

    def test_read_file(self):
        """测试 read_file 方法是否能够正确读取文件"""
        FileUtil.write_file(self.test_file, "Read me!")
        content = FileUtil.read_file("E:\\projectfactory\\AutoStack\\workspace\\student_manage\\resources\\entity\\entity_list.json")
        print(json.loads(content[0]))
        self.assertEqual(content, "Read me!")

    def test_get_template(self):
        """测试 get_template 方法是否能够读取模板文件"""
        template_content = "Hello, ${name}!"
        template_file = self.test_dir / "template.txt"
        FileUtil.write_file(template_file, template_content)

        template = FileUtil.get_template(template_file)
        result = template.substitute(name="World")
        self.assertEqual(result, "Hello, World!")

    def test_copy_all_files(self):
        """测试 copy_all_files 方法是否能够正确复制文件"""
        src_dir = self.test_dir / "src"
        dest_dir = self.test_dir / "dest"
        os.makedirs(src_dir)
        src_file = src_dir / "file.txt"
        FileUtil.write_file(src_file, "Content to copy")

        FileUtil.copy_all_files(str(src_dir), str(dest_dir))

        copied_file = dest_dir / "file.txt"
        with open(copied_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "Content to copy")

    def test_generate_env(self):
        """测试 generate_env 方法是否能够正确生成 .env 文件"""
        env_dict = {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
        }
        FileUtil.generate_env(env_dict, self.test_env_file)

        with open(self.test_env_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("DB_HOST=localhost", content)
        self.assertIn("DB_PORT=5432", content)


if __name__ == "__main__":
    unittest.main()
