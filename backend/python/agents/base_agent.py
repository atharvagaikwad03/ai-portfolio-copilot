"""Base agent class for multi-agent system."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from config.settings import settings


class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system."""

    _global_llm_disabled_reason: Optional[str] = None
    
    def __init__(
        self,
        name: str,
        system_prompt: str,
        model_name: Optional[str] = None,
        temperature: float = None
    ):
        """Initialize base agent."""
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
            model=model_name or settings.LLM_MODEL,
            temperature=temperature or settings.TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.conversation_history: List[BaseMessage] = []
        self._fallback_model = "gpt-4o-mini"
        self._fallback_activated = False
        self._llm_disabled_reason: Optional[str] = None
    
    def _build_messages(self, user_input: str) -> List[BaseMessage]:
        """Build message list with system prompt and conversation history."""
        messages = [SystemMessage(content=self.system_prompt)]
        messages.extend(self.conversation_history)
        messages.append(HumanMessage(content=user_input))
        return messages
    
    def add_to_history(self, user_message: str, ai_message: str):
        """Add messages to conversation history."""
        self.conversation_history.append(HumanMessage(content=user_message))
        self.conversation_history.append(AIMessage(content=ai_message))
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []

    def _mark_llm_unavailable(self, error: Exception):
        """Disable LLM usage for the current process after terminal provider failures."""
        error_text = str(error).lower()
        terminal_tokens = (
            "insufficient_quota",
            "invalid_api_key",
            "incorrect_api_key",
            "authentication",
            "api key",
            "billing",
            "model_not_found",
            "does not exist",
            "connection error",
            "api connection",
        )
        if any(token in error_text for token in terminal_tokens):
            reason = "LLM provider unavailable; using local portfolio fallback."
            self._llm_disabled_reason = reason
            BaseAgent._global_llm_disabled_reason = reason

    def _invoke_llm(self, messages: List[BaseMessage]):
        """Invoke LLM with automatic fallback if configured model is unavailable."""
        disabled_reason = self._llm_disabled_reason or BaseAgent._global_llm_disabled_reason
        if disabled_reason:
            raise RuntimeError(disabled_reason)
        try:
            return self.llm.invoke(messages)
        except Exception as e:
            error_text = str(e).lower()
            should_fallback = (
                not self._fallback_activated
                and self._fallback_model
                and self.llm.model_name != self._fallback_model
                and ("model_not_found" in error_text or "does not exist" in error_text)
            )
            if should_fallback:
                try:
                    self.llm = ChatOpenAI(
                        model=self._fallback_model,
                        temperature=self.llm.temperature,
                        openai_api_key=settings.OPENAI_API_KEY
                    )
                    self._fallback_activated = True
                    return self.llm.invoke(messages)
                except Exception as fallback_error:
                    self._mark_llm_unavailable(fallback_error)
                    raise fallback_error
            self._mark_llm_unavailable(e)
            raise
    
    @abstractmethod
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process user input and return response."""
        pass
    
    def __call__(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Make agent callable."""
        return self.process(user_input, context)
