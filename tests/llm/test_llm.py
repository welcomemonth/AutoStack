import unittest
from unittest.mock import patch, MagicMock
from autostack.llm import LLM
from autostack.llm.schema import Message

class TestLLM(unittest.TestCase):

    @patch('llm.os.getenv')
    def test_init_with_env_variables(self, mock_getenv):
        mock_getenv.side_effect = lambda key, default=None: {
            "LLM_API_KEY": "env_api_key",
            "LLM_BASE_URL": "env_base_url",
            "LLM_SYSTEM_PROMPT": "env_system_prompt",
            "LLM_MODEL": "env_model"
        }.get(key, default)

        llm = LLM()
        self.assertEqual(llm.api_key, "env_api_key")
        self.assertEqual(llm.base_url, "env_base_url")
        self.assertEqual(llm.system_prompt, "env_system_prompt")
        self.assertEqual(llm.model, "env_model")

    def test_init_with_parameters(self):
        llm = LLM(api_key="param_api_key", base_url="param_base_url", system_prompt="param_system_prompt", model="param_model")
        self.assertEqual(llm.api_key, "param_api_key")
        self.assertEqual(llm.base_url, "param_base_url")
        self.assertEqual(llm.system_prompt, "param_system_prompt")
        self.assertEqual(llm.model, "param_model")

    @patch('llm.litellm.completion')
    def test_completion(self, mock_completion):
        mock_completion.return_value = "mocked_response"
        llm = LLM(api_key="test_api_key", base_url="test_base_url", system_prompt="test_system_prompt", model="test_model")
        messages = ["Hello, world!"]
        response = llm.completion(messages)
        self.assertEqual(response, "mocked_response")
        mock_completion.assert_called_once_with(
            model="test_model",
            messages=[{"role": "user", "content": "Hello, world!"}],
            api_base="test_base_url",
            api_key="test_api_key"
        )

    def test_format_msg(self):
        llm = LLM()
        messages = ["Hello, world!", {"role": "user", "content": "Hi!"}, Message(role="user", content="Hey!")]
        formatted_messages = llm.format_msg(messages)
        expected_messages = [
            {"role": "user", "content": "Hello, world!"},
            {"role": "user", "content": "Hi!"},
            {"role": "user", "content": "Hey!"}
        ]
        self.assertEqual(formatted_messages, expected_messages)

if __name__ == "__main__":
    unittest.main()