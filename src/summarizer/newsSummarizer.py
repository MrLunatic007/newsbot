from huggingface_hub import InferenceClient, InferenceEndpointError
from dotenv import load_dotenv
import os

load_dotenv()


class NewsSummarizerError(Exception):
    """Gets raised when generating a summary"""

    pass


class NewsSummarizer:
    MODEL = "Falconsai/text_summarization"

    def __init__(self) -> None:
        self.client = self._model_initialization()

    def _model_initialization(self) -> InferenceClient:
        """Initializes the summarization model"""
        try:
            api_key = os.getenv("HF_TOKEN")
            if not api_key:
                raise NewsSummarizerError("HF_TOKEN not found in environment variables")

            client = InferenceClient(
                provider="hf-inference", api_key=api_key, model=self.MODEL
            )
            return client
        except InferenceEndpointError as e:
            raise NewsSummarizerError(
                f"An inference Endpoint error occurred. Details: {e}"
            )
        except Exception as e:
            raise NewsSummarizerError(
                f"Unknown error occurred initializing the model. Details: {e}"
            )

    def summarizer(self, article: str) -> str:
        """Summarizes the page"""
        try:
            if not article or len(article.strip()) == 0:
                raise NewsSummarizerError("Article content is empty")

            # Truncate if article is too long (many models have token limits)
            max_length = 10000  # Adjust based on model limits
            if len(article) > max_length:
                article = article[:max_length]

            summary = self.client.summarization(article)

            # Handle different possible response formats
            if isinstance(summary, list) and len(summary) > 0:
                if isinstance(summary[0], dict) and "summary_text" in summary[0]:
                    return summary[0]["summary_text"]
                elif isinstance(summary[0], str):
                    return summary[0]
            elif isinstance(summary, dict) and "summary_text" in summary:
                return summary["summary_text"]
            elif isinstance(summary, str):
                return summary
            else:
                raise NewsSummarizerError(
                    f"Unexpected response format: {type(summary)}"
                )

        except Exception as e:
            raise NewsSummarizerError(
                f"A summarization error occurred during summarization. Details: {e}"
            )
