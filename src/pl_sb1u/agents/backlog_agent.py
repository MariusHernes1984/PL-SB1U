"""Backlog agent for managing user stories, epics and prioritization."""

from langchain_core.messages import AIMessage

from pl_sb1u.agents.base import BaseAgent
from pl_sb1u.state import AgentState

BACKLOG_SYSTEM_PROMPT = """Du er en erfaren produktleder-assistent spesialisert på backlog-håndtering for SpareBank 1 Utvikling (SB1U).

Du hjelper med:
- Skrive og raffinere user stories på formatet: "Som <rolle> ønsker jeg <funksjonalitet> slik at <verdi>"
- Definere akseptansekriterier (Gherkin: Gitt / Når / Så)
- Prioritere backlog med MoSCoW (Must have, Should have, Could have, Won't have)
- Beregne WSJF-score (Weighted Shortest Job First): WSJF = CoD / Jobbstørrelse
  - Cost of Delay (CoD) = Forretningsverdi + Tidskritiskhet + Risiko/Mulighet-reduksjon + Åpning for ny verdi
- Estimere relativ kompleksitet (story points: Fibonacci-sekvens 1, 2, 3, 5, 8, 13, 21)
- Definere Definition of Ready (DoR) og Definition of Done (DoD)
- Sprintplanlegging basert på teamkapasitet og velocity

Kontekst: Du jobber i en digital bank / fintech-kontekst med fokus på mobilbank, nettbank, betalingsløsninger og finansielle produkter.

{language_instruction}

Gi alltid strukturerte, actionable svar med konkrete forslag.
"""


class BacklogAgent(BaseAgent):
    """Specialist agent for backlog management and user story crafting."""

    @property
    def name(self) -> str:
        return "backlog"

    @property
    def system_prompt(self) -> str:
        return BACKLOG_SYSTEM_PROMPT.format(language_instruction=self._language_instruction())

    def run(self, state: AgentState) -> AgentState:
        """Process backlog-related requests and return structured output."""
        content = self._invoke_llm(state)
        return AgentState(
            messages=state.messages + [AIMessage(content=content, name="backlog")],
            next_agent="",
            context={**state.context, "last_agent": "backlog"},
            user_input=state.user_input,
            final_response=content,
        )
