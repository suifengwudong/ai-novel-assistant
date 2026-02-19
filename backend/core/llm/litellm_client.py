"""
统一大模型接入层（基于LiteLLM）
支持：OpenAI / Claude / 通义千问 / Ollama
"""

from typing import AsyncGenerator, Optional

import litellm
from litellm import ModelResponse, acompletion
from loguru import logger

from config.settings import settings


class LiteLLMClient:
    """统一大模型客户端"""

    def __init__(self):
        """初始化LLM客户端"""
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS

        # 配置LiteLLM
        if self.base_url:
            litellm.api_base = self.base_url

        logger.info(f"LLM客户端初始化: {self.provider} / {self.model}")

    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        format: Optional[str] = None,
    ) -> str:
        """
        生成文本

        Args:
            prompt: 用户提示
            system_message: 系统消息（可选）
            temperature: 温度参数（可选）
            max_tokens: 最大Token数（可选）
            format: 输出格式（json/text）

        Returns:
            str: 生成的文本
        """
        logger.info(f"调用LLM生成: {self.model}")

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        try:
            response: ModelResponse = await acompletion(
                model=self.model,
                messages=messages,
                api_key=self.api_key,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                response_format={"type": format} if format == "json" else None,
            )

            content = response.choices[0].message.content

            # 记录Token使用
            usage = response.usage
            logger.info(
                f"✅ 生成完成 | "
                f"Tokens: {usage.total_tokens} "
                f"(prompt: {usage.prompt_tokens}, "
                f"completion: {usage.completion_tokens})"
            )

            return content

        except Exception as e:
            logger.error(f"❌ LLM调用失败: {e}")
            raise

    async def generate_stream(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncGenerator[str, None]:
        """
        流式生成文本

        Args:
            prompt: 用户提示
            system_message: 系统消息（可选）
            temperature: 温度参数（可选）
            max_tokens: 最大Token数（可选）

        Yields:
            str: 生成的文本片段
        """
        logger.info(f"调用LLM流式生成: {self.model}")

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                api_key=self.api_key,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True,
            )

            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            logger.info("✅ 流式生成完成")

        except Exception as e:
            logger.error(f"❌ LLM流式调用失败: {e}")
            raise

    async def count_tokens(self, text: str) -> int:
        """
        计算Token数量

        Args:
            text: 文本内容

        Returns:
            int: Token数量
        """
        try:
            return litellm.token_counter(model=self.model, text=text)
        except:
            # 如果无法精确计算，使用近似估计（1 Token ≈ 4 字符）
            return len(text) // 4
