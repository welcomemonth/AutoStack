import re
from string import Template
from autostack.const import PROMPT_ROOT


def prompt_handle(prompt_name, *args):
    # 读取 prompt 文件内容
    with open(PROMPT_ROOT / prompt_name, 'r', encoding='utf-8') as file:
        prompt_template = file.read()

    # 查找所有被 {} 包括的变量名
    variables = re.findall(r'\{(.*?)\}', prompt_template)

    # 进行文本替换
    for i, var in enumerate(variables):
        if i < len(args):
            prompt_template = prompt_template.replace(f'{{{var}}}', args[i])

    return prompt_template
