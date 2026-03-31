"""Base agent class with shared functionality."""

from abc import ABC, abstractmethod

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI

from pl_sb1u.config import get_settings
from pl_sb1u.state import AgentState


class BaseAgent(ABC):
    """Abstract base class for all agents in the multi-agent system."""

    def __init__(self) -> None:
        settings = get_settings()
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.temperature,
            api_key=settings.openai_api_key,
        )
        self.language = settings.language
        self.team_name = settings.team_name

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique agent identifier used in the graph."""

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt that defines the agent's role and behaviour."""

    def _language_instruction(self) -> str:
        if self.language == "no":
            return "Svar alltid på norsk med mindre brukeren spesifikt ber om et annet språk."
        return "Always respond in English unless the user explicitly requests another language."

    @abstractmethod
    def run(self, state: AgentState) -> AgentState:
        """Execute the agent logic and return the updated state."""

    def _build_messages(self, state: AgentState) -> list:
        from langchain_core.messages import SystemMessage

        return [SystemMessage(content=self.system_prompt), *state.messages]

    def _invoke_llm(self, state: AgentState) -> str:
        messages = self._build_messages(state)
        response: AIMessage = self.llm.invoke(messages)
        return str(response.content)
