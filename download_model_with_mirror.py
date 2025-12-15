from huggingface_hub import snapshot_download
import os

# 设置下载目录
download_dir = "/opt/maxkb-app/model/embedding/aspire/acge_text_embedding"

# 确保目录存在
os.makedirs(download_dir, exist_ok=True)

print(f"开始下载模型到: {download_dir}")

# 使用HF-Mirror下载模型
snapshot_download(
    repo_id="aspire/acge_text_embedding",
    local_dir=download_dir,
    local_dir_use_symlinks=False,
    resume_download=True,
    # 使用HF-Mirror
    endpoint="https://hf-mirror.com"
)

print("模型下载完成！")
