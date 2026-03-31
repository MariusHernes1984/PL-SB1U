"""Tests for the orchestrator agent routing logic."""

import json
from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from pl_sb1u.agents.orchestrator import OrchestratorAgent
from pl_sb1u.state import AgentState


@pytest.fixture
def orchestrator() -> OrchestratorAgent:
    with patch("pl_sb1u.agents.base.ChatOpenAI"):
        return OrchestratorAgent()


def _make_state(text: str) -> AgentState:
    return AgentState(messages=[HumanMessage(content=text)], user_input=text)


class TestOrchestratorRouting:
    """Tests for the orchestrator's _parse_agent_name method."""

    @pytest.mark.parametrize(
        "raw, expected",
        [
            ('{"agent": "backlog", "reason": "user story"}', "backlog"),
            ('{"agent": "analytics", "reason": "metrics"}', "analytics"),
            ('{"agent": "communication", "reason": "report"}', "communication"),
            ('{"agent": "research", "reason": "market"}', "research"),
            # Handles extra whitespace / capitalisation
            ('{"agent": "  Backlog  ", "reason": "x"}', "backlog"),
            # Falls back to keyword matching when JSON is malformed
            ("backlog agent should handle this", "backlog"),
            ("analytics data needed", "analytics"),
            # Completely unknown → default to backlog
            ("completely unrelated text xyz", "backlog"),
        ],
    )
    def test_parse_agent_name(
        self, orchestrator: OrchestratorAgent, raw: str, expected: str
    ) -> None:
        assert orchestrator._parse_agent_name(raw) == expected

    def test_run_returns_updated_state(self, orchestrator: OrchestratorAgent) -> None:
        """run() should set next_agent based on LLM response."""
        orchestrator.llm = MagicMock()
        orchestrator.llm.invoke.return_value = AIMessage(
            content='{"agent": "analytics", "reason": "KPI question"}'
        )

        state = _make_state("What is our NPS score?")
        result = orchestrator.run(state)

        assert result.next_agent == "analytics"
        # The orchestrator's AIMessage is appended to the history
        last_msg = result.messages[-1]
        assert isinstance(last_msg, AIMessage)
        assert last_msg.name == "orchestrator"

    def test_run_defaults_to_backlog_on_unknown_response(
        self, orchestrator: OrchestratorAgent
    ) -> None:
        orchestrator.llm = MagicMock()
        orchestrator.llm.invoke.return_value = AIMessage(content="I don't know")

        state = _make_state("Tell me something")
        result = orchestrator.run(state)

        assert result.next_agent == "backlog"
