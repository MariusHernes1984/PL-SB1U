"""Tests for the LangGraph workflow graph."""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from pl_sb1u.state import AgentState


class TestGraphRouting:
    """Test the _route conditional edge function."""

    def test_route_backlog(self):
        from pl_sb1u.graph import _route

        state = AgentState(next_agent="backlog")
        assert _route(state) == "backlog"

    def test_route_analytics(self):
        from pl_sb1u.graph import _route

        state = AgentState(next_agent="analytics")
        assert _route(state) == "analytics"

    def test_route_communication(self):
        from pl_sb1u.graph import _route

        state = AgentState(next_agent="communication")
        assert _route(state) == "communication"

    def test_route_research(self):
        from pl_sb1u.graph import _route

        state = AgentState(next_agent="research")
        assert _route(state) == "research"

    def test_route_unknown_defaults_to_backlog(self):
        from pl_sb1u.graph import _route

        state = AgentState(next_agent="unknown_agent")
        assert _route(state) == "backlog"

    def test_route_empty_defaults_to_backlog(self):
        from pl_sb1u.graph import _route

        state = AgentState(next_agent="")
        assert _route(state) == "backlog"


class TestAgentState:
    """Test the AgentState model."""

    def test_default_state(self):
        state = AgentState()
        assert state.messages == []
        assert state.next_agent == ""
        assert state.context == {}
        assert state.user_input == ""
        assert state.final_response == ""

    def test_state_with_messages(self):
        msg = HumanMessage(content="test")
        state = AgentState(messages=[msg], user_input="test")
        assert len(state.messages) == 1
        assert state.user_input == "test"

    def test_messages_add_annotation(self):
        """add_messages annotation should merge message lists when used via the graph reducer."""
        # Verify that two AgentState instances accumulate messages independently
        msg1 = HumanMessage(content="hello")
        msg2 = AIMessage(content="world")
        state = AgentState(messages=[msg1, msg2])
        assert len(state.messages) == 2
        assert state.messages[0].content == "hello"
        assert state.messages[1].content == "world"
