import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

# 載入環境變數
load_dotenv()

# 從環境變數取得設定
API_BASE                     = os.getenv("LITELLM_MODEL_API_BASE")
API_KEY                      = os.getenv("LITELLM_MODEL_API_KEY")
MODEL_NAME                   = os.getenv("LITELLM_MODEL_MODEL_NAME")

if bool(os.getenv("LITELLM_MODEL_SPECIAL_TOKENS")):
    # 初始化 LiteLlm 模型
    litellm_model = LiteLlm(
        model=MODEL_NAME,
        api_base=API_BASE,
        api_key=API_KEY,
    )
else:
    # 初始化 LiteLlm 模型，並設定 skip_special_tokens 為 False
    litellm_model = LiteLlm(
        model=MODEL_NAME,
        api_base=API_BASE,
        api_key=API_KEY,
        extra_body={"skip_special_tokens": False}
    )