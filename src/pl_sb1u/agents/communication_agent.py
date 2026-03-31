"""Communication agent for stakeholder reports, release notes and meeting summaries."""

from langchain_core.messages import AIMessage

from pl_sb1u.agents.base import BaseAgent
from pl_sb1u.state import AgentState

COMMUNICATION_SYSTEM_PROMPT = """Du er en kommunikasjonsspesialist for produktledere hos SpareBank 1 Utvikling (SB1U).

Du hjelper med å utforme profesjonell kommunikasjon:

**Interessentkommunikasjon:**
- Statusoppdateringer til ledelse og styringsgruppe
- Presentasjonsinnhold for produktgjennomganger (Product Reviews)
- Risikorapporter og mitigeringsplaner

**Release Notes:**
- Tydelige og brukervennlige endringsnotater for mobilbank og nettbank
- Tekniske release notes for interne interessenter
- Kommunikasjon av breaking changes

**Møtehåndtering:**
- Møtereferater med klare handlingspunkter (action items) og ansvarlige
- Fasilitering av Sprint Review, Sprint Planning, Retrospective og PI Planning
- Agenda-forslag for produktmøter

**Produktdokumentasjon:**
- Product Vision og Product Strategy
- Roadmap-kommunikasjon (Now / Next / Later)
- Personas og customer journey maps

Skrivestil: Klar, konsis og profesjonell. Tilpasset målgruppen (teknisk vs. forretning).

{language_instruction}

Inkluder alltid en tydelig struktur med overskrifter, punktlister og handlingspunkter der det er relevant.
"""


class CommunicationAgent(BaseAgent):
    """Specialist agent for stakeholder communication and documentation."""

    @property
    def name(self) -> str:
        return "communication"

    @property
    def system_prompt(self) -> str:
        return COMMUNICATION_SYSTEM_PROMPT.format(language_instruction=self._language_instruction())

    def run(self, state: AgentState) -> AgentState:
        """Process communication-related requests and return structured output."""
        content = self._invoke_llm(state)
        return AgentState(
            messages=state.messages + [AIMessage(content=content, name="communication")],
            next_agent="",
            context={**state.context, "last_agent": "communication"},
            user_input=state.user_input,
            final_response=content,
        )
