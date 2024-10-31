import unittest
from pathlib import Path
import tempfile
import yaml
from segmapy.utils.yaml_model import YamlModel, YamlModelWithoutDefault

class TestYamlModel(unittest.TestCase):
    def setUp(self):
        # 创建一个 YamlModel 的子类实例
        self.model = YamlModel()
        self.model.some_attribute = "test_value"

    def test_to_yaml_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = Path(temp_file.name)
        
        # 调用 to_yaml_file 方法
        self.model.to_yaml_file(temp_file_path)
        
        # 读取临时文件内容并验证其正确性
        with open(temp_file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            self.assertEqual(data['some_attribute'], "test_value")

    def test_check_not_default_config(self):
        with self.assertRaises(ValueError):
            YamlModelWithoutDefault.check_not_default_config({"some_key": "YOUR_DEFAULT_VALUE"})

if __name__ == "__main__":
    unittest.main()