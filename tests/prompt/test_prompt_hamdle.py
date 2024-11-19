from autostack.prompt.prompt_handle import prompt_handle
from autostack.const import PROMPT_ROOT

template_path = PROMPT_ROOT / 'gen_req.prompt'
replacements = {
    'project_name': 'AI Project'
}
product_requirements = prompt_handle(template_path, replacements)
print(product_requirements)