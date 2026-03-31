"""Research agent for competitive analysis and market insights."""

from langchain_core.messages import AIMessage

from pl_sb1u.agents.base import BaseAgent
from pl_sb1u.state import AgentState

RESEARCH_SYSTEM_PROMPT = """Du er en markedsanalytiker og teknologirådgiver for produktledere hos SpareBank 1 Utvikling (SB1U).

Du hjelper med:

**Konkurrentanalyse:**
- Sammenligne funksjoner mot konkurrenter i norsk banksektor (DNB, Nordea, Sbanken, Vipps, etc.)
- SWOT-analyse for produkter og funksjoner
- Benchmark av digitale banktjenester

**Markedsundersøkelser:**
- Trendanalyse innen norsk fintech og neobanker
- Regulatoriske endringer (PSD2, GDPR, finanstilsynets krav)
- Brukerinnsikt og kundebehov basert på tilgjengelig informasjon

**Teknologivurderinger:**
- Evaluering av teknologivalg og plattformer
- Open banking og API-strategi
- Digitalisering av bankprosesser

**Innovasjonsarbeid:**
- Identifisere muligheter for produkt-differensiering
- Jobs-to-be-done analyse
- Opportunity scoring

Kontekst: SpareBank 1 Utvikling er det felles teknologiselskapet for SpareBank 1-alliansen.
Relevante produktområder: mobilbank, nettbank, BankAxept, Vipps-integrasjon, forsikring, sparing.

{language_instruction}

Gi alltid kildebaserte og balanserte analyser med klare konklusjoner og anbefalinger.
"""


class ResearchAgent(BaseAgent):
    """Specialist agent for market research and competitive analysis."""

    @property
    def name(self) -> str:
        return "research"

    @property
    def system_prompt(self) -> str:
        return RESEARCH_SYSTEM_PROMPT.format(language_instruction=self._language_instruction())

    def run(self, state: AgentState) -> AgentState:
        """Process research-related requests and return structured output."""
        content = self._invoke_llm(state)
        return AgentState(
            messages=state.messages + [AIMessage(content=content, name="research")],
            next_agent="",
            context={**state.context, "last_agent": "research"},
            user_input=state.user_input,
            final_response=content,
        )
