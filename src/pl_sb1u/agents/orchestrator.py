"""Orchestrator agent that routes requests to the appropriate specialist agent."""

import json
import re

from langchain_core.messages import AIMessage

from pl_sb1u.agents.base import BaseAgent
from pl_sb1u.state import AgentState

ROUTING_PROMPT = """Du er koordinatoren i et multi-agent system for en produktleder hos SpareBank 1 Utvikling (SB1U).

Din eneste oppgave er å analysere brukerens forespørsel og bestemme hvilken spesialistagent som skal håndtere den.

Tilgjengelige agenter:
- backlog: Håndterer user stories, backlog-prioritering (MoSCoW, WSJF), akseptansekriterier og sprintplanlegging.
- analytics: Analyserer KPIer, sprintmetrikker, burndown-data og produktytelse.
- communication: Utformer interessentkommunikasjon, møtereferater, release notes og statusrapporter.
- research: Utfører konkurrentanalyse, markedsundersøkelser og teknologivurderinger.

Svar KUN med et JSON-objekt på følgende format (ingen annen tekst):
{{"agent": "<agent_navn>", "reason": "<kort begrunnelse på norsk>"}}

{language_instruction}
"""


class OrchestratorAgent(BaseAgent):
    """Routes incoming requests to the most appropriate specialist agent."""

    @property
    def name(self) -> str:
        return "orchestrator"

    @property
    def system_prompt(self) -> str:
        return ROUTING_PROMPT.format(language_instruction=self._language_instruction())

    def run(self, state: AgentState) -> AgentState:
        """Determine which agent should handle the user's request."""
        messages = self._build_messages(state)
        response: AIMessage = self.llm.invoke(messages)
        raw = str(response.content).strip()

        agent_name = self._parse_agent_name(raw)

        return AgentState(
            messages=state.messages + [AIMessage(content=raw, name="orchestrator")],
            next_agent=agent_name,
            context=state.context,
            user_input=state.user_input,
            final_response=state.final_response,
        )

    def _parse_agent_name(self, raw: str) -> str:
        """Extract agent name from the LLM response JSON."""
        valid_agents = {"backlog", "analytics", "communication", "research"}
        try:
            # Try to extract JSON even if surrounded by extra text
            match = re.search(r"\{.*?\}", raw, re.DOTALL)
            if match:
                data = json.loads(match.group())
                agent = data.get("agent", "").lower().strip()
                if agent in valid_agents:
                    return agent
        except (json.JSONDecodeError, AttributeError):
            pass

        # Fallback: keyword matching
        lower = raw.lower()
        for agent in valid_agents:
            if agent in lower:
                return agent

        return "backlog"  # safe default
