"""Analytics agent for KPIs, sprint metrics and product performance."""

from langchain_core.messages import AIMessage

from pl_sb1u.agents.base import BaseAgent
from pl_sb1u.state import AgentState

ANALYTICS_SYSTEM_PROMPT = """Du er en dataanalytiker-assistent spesialisert på produktmetrikker og KPIer for SpareBank 1 Utvikling (SB1U).

Du hjelper med å:
- Definere og følge opp North Star Metric og støttende KPIer
- Analysere sprintdata: velocity, burndown, gjennomstrømningstid (cycle time), lead time
- Tolke produktytelse: konverteringsrater, brukerengasjement, frafallsanalyse (churn)
- Sette opp OKR-er (Objectives and Key Results) med målbare nøkkelresultater
- Gjennomføre retrospektiv-analyser basert på sprint-data
- Identifisere flaskehalser ved hjelp av kumulativt flytdiagram (CFD) og Kanban-metrikker
- Beregne ROI og business case for produktforbedringer
- Presentere data visuelt (beskrive tabeller, grafer og dashbord)

Relevante fintech KPIer:
- Monthly Active Users (MAU) / Daily Active Users (DAU)
- Feature adoption rate
- Net Promoter Score (NPS)
- Time to market
- Defect escape rate
- Customer Lifetime Value (CLV)

{language_instruction}

Gi alltid konkrete tall-eksempler og visualiseringsbeskrivelser der det er relevant.
"""


class AnalyticsAgent(BaseAgent):
    """Specialist agent for product analytics, KPIs and sprint metrics."""

    @property
    def name(self) -> str:
        return "analytics"

    @property
    def system_prompt(self) -> str:
        return ANALYTICS_SYSTEM_PROMPT.format(language_instruction=self._language_instruction())

    def run(self, state: AgentState) -> AgentState:
        """Process analytics-related requests and return structured output."""
        content = self._invoke_llm(state)
        return AgentState(
            messages=state.messages + [AIMessage(content=content, name="analytics")],
            next_agent="",
            context={**state.context, "last_agent": "analytics"},
            user_input=state.user_input,
            final_response=content,
        )
