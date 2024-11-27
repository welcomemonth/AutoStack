import unittest
from autostack.utils.markdown_util import MarkdownUtil


class TestMarkdownUtil(unittest.TestCase):

    def test_parse_code_block_with_language(self):
        # 测试包含指定语言的代码块
        content = """
        Here is some text before the code block.

        ```python
        def hello_world():
            print("Hello, world!")
        ```

        And some text after the code block.
        """
        expected_output = ['def hello_world():\n    print("Hello, world!")']
        actual_output = MarkdownUtil.parse_code_block(content, 'python')
        self.assertEqual(actual_output, expected_output)

    def test_parse_code_block_without_language(self):
        # 测试不包含指定语言的代码块
        content = """
        Here is some text before the code block.

        ```javascript
        function helloWorld() {
            console.log("Hello, world!");
        }
        ```

        And some text after the code block.
        """
        expected_output = []
        actual_output = MarkdownUtil.parse_code_block(content, 'python')
        self.assertEqual(actual_output, expected_output)

    def test_parse_code_block_no_code_block(self):
        # 测试没有代码块的情况
        content = "This is a simple text without any code blocks."
        expected_output = [content]
        actual_output = MarkdownUtil.parse_code_block(content, 'python')
        self.assertEqual(actual_output, expected_output)

    def test_parse_code_block_multiple_code_blocks(self):
        # 测试多个代码块的情况
        content = """
        Here is some text before the code block.

        ```python
        def hello_world():
            print("Hello, world!")
        ```

        And another code block:

        ```python
        def goodbye_world():
            print("Goodbye, world!")
        ```

        And some text after the code block.
        """
        expected_output = [
            'def hello_world():\n    print("Hello, world!")',
            'def goodbye_world():\n    print("Goodbye, world!")'
        ]
        actual_output = MarkdownUtil.parse_code_block(content, 'python')
        self.assertEqual(actual_output, expected_output)

    def test_parse_code_block_with_no_matching_language(self):
        # 测试没有匹配的语言
        content = """
        Here is some text before the code block.

        ```python
        def hello_world():
            print("Hello, world!")
        ```

        And some text after the code block.
        """
        expected_output = [content]
        actual_output = MarkdownUtil.parse_code_block(content, 'javascript')
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
