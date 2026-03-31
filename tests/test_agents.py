"""Tests for specialist agents."""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from pl_sb1u.agents.analytics_agent import AnalyticsAgent
from pl_sb1u.agents.backlog_agent import BacklogAgent
from pl_sb1u.agents.communication_agent import CommunicationAgent
from pl_sb1u.agents.research_agent import ResearchAgent
from pl_sb1u.state import AgentState


def _make_state(text: str) -> AgentState:
    return AgentState(messages=[HumanMessage(content=text)], user_input=text)


def _patch_llm(agent, response: str) -> None:
    agent.llm = MagicMock()
    agent.llm.invoke.return_value = AIMessage(content=response)


@pytest.fixture
def backlog_agent():
    with patch("pl_sb1u.agents.base.ChatOpenAI"):
        return BacklogAgent()


@pytest.fixture
def analytics_agent():
    with patch("pl_sb1u.agents.base.ChatOpenAI"):
        return AnalyticsAgent()


@pytest.fixture
def communication_agent():
    with patch("pl_sb1u.agents.base.ChatOpenAI"):
        return CommunicationAgent()


@pytest.fixture
def research_agent():
    with patch("pl_sb1u.agents.base.ChatOpenAI"):
        return ResearchAgent()


class TestAgentNames:
    def test_backlog_name(self, backlog_agent):
        assert backlog_agent.name == "backlog"

    def test_analytics_name(self, analytics_agent):
        assert analytics_agent.name == "analytics"

    def test_communication_name(self, communication_agent):
        assert communication_agent.name == "communication"

    def test_research_name(self, research_agent):
        assert research_agent.name == "research"


class TestBacklogAgent:
    def test_run_returns_final_response(self, backlog_agent):
        _patch_llm(backlog_agent, "Som bruker ønsker jeg å se saldo...")
        state = _make_state("Skriv en user story for å se saldo")
        result = backlog_agent.run(state)

        assert result.final_response == "Som bruker ønsker jeg å se saldo..."
        assert result.context["last_agent"] == "backlog"
        assert result.next_agent == ""

    def test_run_appends_ai_message(self, backlog_agent):
        _patch_llm(backlog_agent, "User story her")
        state = _make_state("user story")
        result = backlog_agent.run(state)

        last = result.messages[-1]
        assert isinstance(last, AIMessage)
        assert last.name == "backlog"


class TestAnalyticsAgent:
    def test_run_returns_final_response(self, analytics_agent):
        _patch_llm(analytics_agent, "NPS-score er 42")
        state = _make_state("Hva er NPS-scoren vår?")
        result = analytics_agent.run(state)

        assert result.final_response == "NPS-score er 42"
        assert result.context["last_agent"] == "analytics"

    def test_system_prompt_contains_kpi(self, analytics_agent):
        assert "KPI" in analytics_agent.system_prompt or "kpi" in analytics_agent.system_prompt.lower()


class TestCommunicationAgent:
    def test_run_returns_final_response(self, communication_agent):
        _patch_llm(communication_agent, "**Statusrapport – Sprint 12**\n\n...")
        state = _make_state("Skriv statusrapport for sprint 12")
        result = communication_agent.run(state)

        assert "Statusrapport" in result.final_response
        assert result.context["last_agent"] == "communication"


class TestResearchAgent:
    def test_run_returns_final_response(self, research_agent):
        _patch_llm(research_agent, "DNB sin mobilapp har feature X...")
        state = _make_state("Sammenlign oss med DNB")
        result = research_agent.run(state)

        assert "DNB" in result.final_response
        assert result.context["last_agent"] == "research"
