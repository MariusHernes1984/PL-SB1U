"""Shared state model for the multi-agent workflow."""

from typing import Annotated, Any

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """Shared state passed between agents in the workflow graph."""

    messages: Annotated[list[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Conversation history for the current session.",
    )
    next_agent: str = Field(
        default="",
        description="Name of the next agent to invoke. Set by the orchestrator.",
    )
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Shared context and artifacts produced by agents.",
    )
    user_input: str = Field(
        default="",
        description="The latest input from the product lead.",
    )
    final_response: str = Field(
        default="",
        description="The final assembled response to present to the user.",
    )
