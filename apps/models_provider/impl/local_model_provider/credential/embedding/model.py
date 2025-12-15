# coding=utf-8
"""
    @project: MaxKB
    @Author：虎虎
    @file： model.py.py
    @date：2025/11/7 14:02
    @desc:
"""
from typing import Dict

from django.utils.translation import gettext_lazy as _, gettext

from common import forms
from common.exception.app_exception import AppApiException
from common.forms import BaseForm
from models_provider.base_model_provider import BaseModelCredential, ValidCode
from models_provider.impl.local_model_provider.model.embedding import LocalEmbedding
from common.utils.logger import maxkb_logger

class LocalEmbeddingCredential(BaseForm, BaseModelCredential):

    def is_valid(self, model_type: str, model_name, model_credential: Dict[str, object], model_params, provider,
                 raise_exception=False):
        if not model_type == 'EMBEDDING':
            raise AppApiException(ValidCode.valid_error.value,
                                  gettext('{model_type} Model type is not supported').format(model_type=model_type))
        for key in ['cache_folder']:
            if key not in model_credential:
                if raise_exception:
                    raise AppApiException(ValidCode.valid_error.value, gettext('{key}  is required').format(key=key))
                else:
                    return False
        try:
            # 检查模型文件是否为Git LFS指针文件
            import os
            model_path = model_name
            if os.path.isdir(model_path):
                # 检查主要模型文件
                for file_name in ['pytorch_model.bin', 'model.safetensors']:
                    file_path = os.path.join(model_path, file_name)
                    if os.path.exists(file_path):
                        # 以二进制模式读取文件开头，避免UTF-8解码错误
                        with open(file_path, 'rb') as f:
                            content = f.read(100)  # 只读取前100字节检查
                        if content.startswith(b'version https://git-lfs.github.com/spec/v1'):
                            raise AppApiException(ValidCode.valid_error.value,
                                                  gettext('Model files are Git LFS pointer files, not actual model data. Please install git-lfs and run `git lfs pull` or download model files directly.'))
            
            model: LocalEmbedding = provider.get_model(model_type, model_name, model_credential)
            model.embed_query(gettext('Hello'))
        except Exception as e:
            maxkb_logger.error(f'Exception: {e}', exc_info=True)
            if isinstance(e, AppApiException):
                raise e
            if raise_exception:
                raise AppApiException(ValidCode.valid_error.value,
                                      gettext(
                                          'Verification failed, please check whether the parameters are correct: {error}').format(
                                          error=str(e)))
            else:
                return False
        return True

    def encryption_dict(self, model: Dict[str, object]):
        return model

    cache_folder = forms.TextInputField(_('Model catalog'), required=True)
