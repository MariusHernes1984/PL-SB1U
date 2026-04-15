"""LangGraph multi-agent workflow for pl-sb1u."""

from typing import Literal

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from pl_sb1u.agents.analytics_agent import AnalyticsAgent
from pl_sb1u.agents.backlog_agent import BacklogAgent
from pl_sb1u.agents.communication_agent import CommunicationAgent
from pl_sb1u.agents.orchestrator import OrchestratorAgent
from pl_sb1u.agents.research_agent import ResearchAgent
from pl_sb1u.state import AgentState

# Node names
ORCHESTRATOR = "orchestrator"
BACKLOG = "backlog"
ANALYTICS = "analytics"
COMMUNICATION = "communication"
RESEARCH = "research"


def _route(state: AgentState) -> Literal["backlog", "analytics", "communication", "research"]:
    """Conditional edge: route to the specialist agent chosen by the orchestrator."""
    agent = state.next_agent
    if agent in {BACKLOG, ANALYTICS, COMMUNICATION, RESEARCH}:
        return agent  # type: ignore[return-value]
    return BACKLOG  # safe default


def build_graph() -> StateGraph:
    """Construct and compile the multi-agent LangGraph workflow."""
    orchestrator = OrchestratorAgent()
    backlog = BacklogAgent()
    analytics = AnalyticsAgent()
    communication = CommunicationAgent()
    research = ResearchAgent()

    graph = StateGraph(AgentState)

    # Register nodes
    graph.add_node(ORCHESTRATOR, orchestrator.run)
    graph.add_node(BACKLOG, backlog.run)
    graph.add_node(ANALYTICS, analytics.run)
    graph.add_node(COMMUNICATION, communication.run)
    graph.add_node(RESEARCH, research.run)

    # Entry point
    graph.set_entry_point(ORCHESTRATOR)

    # Orchestrator routes to one specialist
    graph.add_conditional_edges(
        ORCHESTRATOR,
        _route,
        {
            BACKLOG: BACKLOG,
            ANALYTICS: ANALYTICS,
            COMMUNICATION: COMMUNICATION,
            RESEARCH: RESEARCH,
        },
    )

    # All specialist agents terminate
    for node in (BACKLOG, ANALYTICS, COMMUNICATION, RESEARCH):
        graph.add_edge(node, END)

    return graph.compile()


def run_workflow(user_input: str, context: dict | None = None) -> AgentState:
    """Run the multi-agent workflow for a single user turn.

    Args:
        user_input: The product lead's question or task.
        context: Optional carry-over context from previous turns.

    Returns:
        The final AgentState containing the response.
    """
    compiled = build_graph()

    initial_state = AgentState(
        messages=[HumanMessage(content=user_input)],
        user_input=user_input,
        context=context or {},
    )

    result = compiled.invoke(initial_state)
    return AgentState(**result)
