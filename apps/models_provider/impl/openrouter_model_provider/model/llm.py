# coding=utf-8
"""
    @project: maxkb
    @Author：AI Assistant
    @file： llm.py
    @date：2025/12/16
    @desc: OpenRouter LLM Model Implementation
"""
from typing import List, Dict

from langchain_core.messages import BaseMessage, get_buffer_string

from common.config.tokenizer_manage_config import TokenizerManage
from models_provider.base_model_provider import MaxKBBaseModel
from models_provider.impl.base_chat_open_ai import BaseChatOpenAI


def custom_get_token_ids(text: str):
    tokenizer = TokenizerManage.get_tokenizer()
    return tokenizer.encode(text)


class OpenRouterChatModel(MaxKBBaseModel, BaseChatOpenAI):

    @staticmethod
    def is_cache_model():
        return False

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(model_kwargs)
        streaming = model_kwargs.get('streaming', True)
        chat_open_ai = OpenRouterChatModel(
            model=model_name,
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=model_credential.get('api_key'),
            extra_body=optional_params,
            streaming=streaming,
            custom_get_token_ids=custom_get_token_ids
        )
        return chat_open_ai

    def get_num_tokens_from_messages(self, messages: List[BaseMessage]) -> int:
        try:
            return super().get_num_tokens_from_messages(messages)
        except Exception as e:
            tokenizer = TokenizerManage.get_tokenizer()
            return sum([len(tokenizer.encode(get_buffer_string([m]))) for m in messages])

    def get_num_tokens(self, text: str) -> int:
        try:
            return super().get_num_tokens(text)
        except Exception as e:
            tokenizer = TokenizerManage.get_tokenizer()
            return len(tokenizer.encode(text))
