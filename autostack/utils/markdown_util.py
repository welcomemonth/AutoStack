import re
from autostack.logs import logger


class MarkdownUtil:
    """
    markdown解析工具
    """

    @staticmethod
    def parse_code_block(content: str, language: str) -> [str]:
        """
        解析 ```xxx {content} ``` 中的具体内容，仅解析最外层，支持解析失败的情况。
        :param content: 输入文本，包含可能的代码块。
        :param language: 指定的代码块语言标记 (xxx)。
        :return: [str]: 解析成功的内容,如果解析失败则原字符串输出。
        """
        # 正则匹配指定语言的最外层代码块
        pattern = rf"```{language}(.*?)```"

        # 使用正则表达式，避免贪婪匹配
        # match = re.search(pattern, content, re.DOTALL)

        # 返回匹配的内容（去掉两端空格）
        matches = re.findall(pattern, content, re.DOTALL)

        if not matches:
            logger.error(f"字符串解析失败：'{language}'.")
            return [content]

        # 返回所有匹配的代码块内容
        return [match.strip() for match in matches]


