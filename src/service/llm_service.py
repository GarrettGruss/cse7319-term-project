import os
import yaml
from datetime import datetime
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from ..model.models import PostSummary, LLMRequest, LLMResponse


class LLMService:
    """Service for generating content using Large Language Models"""

    def __init__(self, default_model: str = "gemini-2.5-pro", default_temperature: float = 0.7):
        """
        Initialize LLM service

        Args:
            default_model: Default model to use for generation
            default_temperature: Default temperature for generation
        """
        self.default_model = default_model
        self.default_temperature = default_temperature
        self._validate_api_key()

    def _validate_api_key(self) -> None:
        """Validate that required API keys are available"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not found")

    def _create_llm_client(self, model: str, temperature: float) -> ChatGoogleGenerativeAI:
        """
        Create LLM client with specified parameters

        Args:
            model: Model name to use
            temperature: Temperature parameter

        Returns:
            ChatGoogleGenerativeAI: Configured LLM client
        """
        api_key = os.getenv("GEMINI_API_KEY")
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature
        )

    def post_summary_to_yaml(self, post_summary: PostSummary) -> str:
        """
        Convert PostSummary to YAML string

        Args:
            post_summary: The post summary to convert

        Returns:
            str: YAML representation of the post summary
        """
        # Convert to dict first to ensure proper serialization
        summary_dict = post_summary.model_dump()
        return yaml.dump(summary_dict, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def generate_linkedin_post(
        self,
        post_summary: PostSummary,
        custom_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> LLMResponse:
        """
        Generate a LinkedIn post from a Reddit post summary

        Args:
            post_summary: The structured post summary
            custom_prompt: Custom prompt (uses default if None)
            model: Model to use (uses default if None)
            temperature: Temperature to use (uses default if None)

        Returns:
            LLMResponse: Generated content and metadata
        """
        # Use defaults if not specified
        model = model or self.default_model
        temperature = temperature or self.default_temperature

        # Default prompt for LinkedIn post generation
        if not custom_prompt:
            custom_prompt = (
                "Generate a short LinkedIn post from this conversation. "
                "Extract the debate or lightbulb moment from this thread and present it. "
                "Make it engaging and professional for a LinkedIn audience."
            )

        # Convert post summary to YAML
        yaml_content = self.post_summary_to_yaml(post_summary)

        # Create LLM request
        llm_request = LLMRequest(
            prompt=custom_prompt,
            context=yaml_content,
            model=model,
            temperature=temperature
        )

        return self.query_llm(llm_request)

    def query_llm(self, llm_request: LLMRequest) -> LLMResponse:
        """
        Query the LLM with a structured request

        Args:
            llm_request: The LLM request containing prompt and context

        Returns:
            LLMResponse: Generated response with metadata

        Raises:
            Exception: If LLM query fails
        """
        try:
            # Create LLM client
            llm = self._create_llm_client(llm_request.model, llm_request.temperature)

            # Combine prompt with context
            full_prompt = f"{llm_request.prompt}\n\nContext:\n{llm_request.context}"

            # Query the model
            response = llm.invoke(full_prompt)

            return LLMResponse(
                content=response.content,
                model_used=llm_request.model,
                timestamp=datetime.utcnow()
            )

        except Exception as e:
            raise Exception(f"Error querying LLM: {e}")

    def generate_custom_content(
        self,
        post_summary: PostSummary,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> LLMResponse:
        """
        Generate custom content with a specific prompt

        Args:
            post_summary: The structured post summary
            prompt: Custom prompt for generation
            model: Model to use (uses default if None)
            temperature: Temperature to use (uses default if None)

        Returns:
            LLMResponse: Generated content and metadata
        """
        return self.generate_linkedin_post(
            post_summary=post_summary,
            custom_prompt=prompt,
            model=model,
            temperature=temperature
        )

    def batch_generate(
        self,
        post_summaries: list[PostSummary],
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> list[LLMResponse]:
        """
        Generate content for multiple post summaries

        Args:
            post_summaries: List of post summaries to process
            prompt: Prompt to use for all generations
            model: Model to use (uses default if None)
            temperature: Temperature to use (uses default if None)

        Returns:
            list[LLMResponse]: List of generated responses
        """
        responses = []
        for post_summary in post_summaries:
            try:
                response = self.generate_custom_content(
                    post_summary=post_summary,
                    prompt=prompt,
                    model=model,
                    temperature=temperature
                )
                responses.append(response)
            except Exception as e:
                # Log error but continue with other summaries
                print(f"Error processing post '{post_summary.post_title}': {e}")
                continue

        return responses