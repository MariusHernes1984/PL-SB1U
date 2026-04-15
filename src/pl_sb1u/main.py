"""CLI entry point for the pl-sb1u multi-agent assistant."""

import sys
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from pl_sb1u.graph import run_workflow

app = typer.Typer(
    name="pl-sb1u",
    help="Multi-agent assistent for produktledere hos SpareBank 1 Utvikling.",
    no_args_is_help=False,
)

console = Console()

AGENT_COLORS = {
    "backlog": "green",
    "analytics": "blue",
    "communication": "magenta",
    "research": "yellow",
}

AGENT_LABELS = {
    "backlog": "🗒️  Backlog-agent",
    "analytics": "📊 Analytics-agent",
    "communication": "💬 Kommunikasjons-agent",
    "research": "🔍 Research-agent",
}


def _print_banner() -> None:
    console.print(
        Panel.fit(
            "[bold blue]PL-SB1U[/bold blue] — Multi-agent assistent for produktledere\n"
            "[dim]SpareBank 1 Utvikling | Skriv 'avslutt' eller 'exit' for å avslutte[/dim]",
            border_style="blue",
        )
    )


def _print_response(response: str, agent_name: str) -> None:
    color = AGENT_COLORS.get(agent_name, "white")
    label = AGENT_LABELS.get(agent_name, agent_name)
    console.print(f"\n[bold {color}]{label}[/bold {color}]")
    console.print(Markdown(response))
    console.print()


@app.command()
def chat(
    query: Optional[str] = typer.Argument(
        None,
        help="Enkelt spørsmål å sende til agenten. Utelat for interaktiv modus.",
    ),
) -> None:
    """Start the interactive multi-agent chat session (or run a single query)."""
    _print_banner()

    if query:
        # Single-shot mode
        with console.status("[bold green]Behandler forespørsel...[/bold green]"):
            state = run_workflow(query)
        _print_response(state.final_response, state.context.get("last_agent", "backlog"))
        return

    # Interactive REPL mode
    context: dict = {}
    console.print("[dim]Tips: Spør om backlog, analyser, kommunikasjon eller forskning.[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]Du[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Avslutter...[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "avslutt", "quit", "q"}:
            console.print("[dim]Ha det bra! 👋[/dim]")
            break

        with console.status("[bold green]Behandler...[/bold green]"):
            try:
                state = run_workflow(user_input, context=context)
            except (ValueError, RuntimeError, OSError) as exc:
                console.print(f"[red]Feil: {exc}[/red]")
                continue

        _print_response(state.final_response, state.context.get("last_agent", "backlog"))
        # Carry forward context for next turn
        context = state.context


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
