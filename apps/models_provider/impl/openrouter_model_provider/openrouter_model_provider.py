# coding=utf-8
"""
    @project: maxkb
    @Author：AI Assistant
    @file： openrouter_model_provider.py
    @date：2025/12/16
    @desc: OpenRouter Model Provider Implementation
"""
import os

from common.utils.common import get_file_content
from models_provider.base_model_provider import IModelProvider, ModelProvideInfo, ModelInfo, \
    ModelTypeConst, ModelInfoManage
from models_provider.impl.openrouter_model_provider.credential.llm import OpenRouterLLMModelCredential
from models_provider.impl.openrouter_model_provider.model.llm import OpenRouterChatModel
from maxkb.conf import PROJECT_DIR
from django.utils.translation import gettext_lazy as _

openrouter_llm_model_credential = OpenRouterLLMModelCredential()
model_info_list = [
    ModelInfo('openai/gpt-3.5-turbo', _('OpenAI GPT-3.5 Turbo'), ModelTypeConst.LLM,
              openrouter_llm_model_credential, OpenRouterChatModel
              ),
    ModelInfo('openai/gpt-4', _('OpenAI GPT-4'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
    ModelInfo('openai/gpt-4o', _('OpenAI GPT-4o'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
    ModelInfo('anthropic/claude-3-opus-20240229', _('Anthropic Claude 3 Opus'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
    ModelInfo('anthropic/claude-3-sonnet-20240229', _('Anthropic Claude 3 Sonnet'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
    ModelInfo('anthropic/claude-3-haiku-20240307', _('Anthropic Claude 3 Haiku'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
    ModelInfo('mistralai/mistral-7b-instruct', _('Mistral 7B Instruct'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
    ModelInfo('mistralai/mixtral-8x7b-instruct', _('Mixtral 8x7B Instruct'), ModelTypeConst.LLM, openrouter_llm_model_credential,
              OpenRouterChatModel),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('openai/gpt-3.5-turbo', _('OpenAI GPT-3.5 Turbo'), ModelTypeConst.LLM,
                                         openrouter_llm_model_credential, OpenRouterChatModel
                                         ))
    .build()
)


class OpenRouterModelProvider(IModelProvider):

    def get_model_info_manage(self):
        return model_info_manage

    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_openrouter_provider', name='OpenRouter', icon=get_file_content(
            os.path.join(PROJECT_DIR, "apps", 'models_provider', 'impl', 'openrouter_model_provider', 'icon',
                         'openrouter_icon_svg')))
