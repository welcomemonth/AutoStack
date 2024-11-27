from autostack.utils import PromptUtil
from autostack.common.const import PROMPT_ROOT
import unittest


class TestPromptHandler(unittest.TestCase):

    def test_prompt_handle(self):
        template_path = PROMPT_ROOT / 'gen_prd.prompt'
        replacements = {
            'project_name': 'AI Project'
        }
        product_requirements = PromptUtil.prompt_handle(template_path, replacements)
        print(product_requirements)
