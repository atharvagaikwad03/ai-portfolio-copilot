"""Base agent class for multi-agent system."""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from config.settings import settings


class BaseAgent(ABC):
    """Base class for all agents in the multi-agent system."""
    
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

    def _invoke_llm(self, messages: List[BaseMessage]):
        """Invoke LLM with automatic fallback if configured model is unavailable."""
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
                self.llm = ChatOpenAI(
                    model=self._fallback_model,
                    temperature=self.llm.temperature,
                    openai_api_key=settings.OPENAI_API_KEY
                )
                self._fallback_activated = True
                return self.llm.invoke(messages)
            raise
    
    @abstractmethod
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process user input and return response."""
        pass
    
    def __call__(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Make agent callable."""
        return self.process(user_input, context)
