"""
AaaS vs SaaS Cost Calculator

Compares the total cost of ownership for traditional SaaS tools
against AI agent replacements using real, current pricing data.

Author: Muhammad Usman Bashir (@BeingOttoman)
License: MIT
"""

from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


@dataclass
class SaaSTool:
    """Represents a SaaS tool with per-seat pricing."""
    name: str
    plan: str
    cost_per_seat: float
    seats: int
    category: str

    @property
    def monthly_cost(self) -> float:
        return self.cost_per_seat * self.seats


@dataclass
class AaaSAgent:
    """Represents an AI agent with usage-based pricing."""
    name: str
    provider: str
    monthly_base_cost: float
    estimated_calls_per_month: int
    category: str

    # API cost components
    stt_cost_per_min: float = 0.0043   # Deepgram Nova-3
    llm_cost_per_min: float = 0.006    # GPT-4o (avg tokens per conversation)
    tts_cost_per_min: float = 0.003    # ElevenLabs Flash v2.5
    avg_call_duration_min: float = 3.0

    @property
    def api_cost_per_call(self) -> float:
        per_min = self.stt_cost_per_min + self.llm_cost_per_min + self.tts_cost_per_min
        return per_min * self.avg_call_duration_min

    @property
    def monthly_api_cost(self) -> float:
        return self.api_cost_per_call * self.estimated_calls_per_month

    @property
    def monthly_cost(self) -> float:
        return self.monthly_base_cost + self.monthly_api_cost


# Default SaaS stack (adjust to your actual subscriptions)
DEFAULT_SAAS_STACK = [
    SaaSTool("Salesforce", "Enterprise", 150.0, 8, "CRM"),
    SaaSTool("Zendesk", "Professional", 89.0, 5, "Support"),
    SaaSTool("Mixpanel", "Growth", 89.0, 1, "Analytics"),
    SaaSTool("Calendly", "Teams", 12.0, 8, "Scheduling"),
    SaaSTool("Intercom", "Pro", 74.0, 3, "Messaging"),
]

# Default AaaS replacement stack
DEFAULT_AAAS_STACK = [
    AaaSAgent("Voice CRM Agent", "LiveKit + GPT-4o", 50.0, 3200, "CRM",
              avg_call_duration_min=4.0),
    AaaSAgent("Voice Support Agent", "LiveKit + Claude", 50.0, 5400, "Support",
              llm_cost_per_min=0.005, avg_call_duration_min=3.5),
    AaaSAgent("Analytics Agent", "Claude API", 50.0, 900, "Analytics",
              stt_cost_per_min=0.0, tts_cost_per_min=0.0, avg_call_duration_min=0.5),
    AaaSAgent("Scheduling Agent", "LiveKit + GPT-4o-mini", 30.0, 1800, "Scheduling",
              llm_cost_per_min=0.0003, avg_call_duration_min=2.0),
]


def run_comparison(
    saas_stack: list[SaaSTool] = DEFAULT_SAAS_STACK,
    aaas_stack: list[AaaSAgent] = DEFAULT_AAAS_STACK,
) -> dict:
    """Run the cost comparison and return results."""
    console = Console()

    # SaaS Table
    saas_table = Table(
        title="[bold cyan]BEFORE — Traditional SaaS Stack[/]",
        title_style="bold",
        border_style="dim",
    )
    saas_table.add_column("Tool", style="white")
    saas_table.add_column("Plan", style="dim")
    saas_table.add_column("Seats", justify="right", style="yellow")
    saas_table.add_column("Monthly Cost", justify="right", style="red")

    total_saas = 0.0
    total_seats = 0
    for tool in saas_stack:
        saas_table.add_row(
            tool.name, tool.plan,
            str(tool.seats), f"${tool.monthly_cost:,.2f}"
        )
        total_saas += tool.monthly_cost
        total_seats += tool.seats

    saas_table.add_section()
    saas_table.add_row(
        "[bold]TOTAL[/]", "", f"[bold]{total_seats}[/]",
        f"[bold red]${total_saas:,.2f}/mo[/]"
    )

    # AaaS Table
    aaas_table = Table(
        title="[bold green]AFTER — AaaS Agent Stack[/]",
        title_style="bold",
        border_style="dim",
    )
    aaas_table.add_column("Agent", style="white")
    aaas_table.add_column("Provider", style="dim")
    aaas_table.add_column("Calls/mo", justify="right", style="cyan")
    aaas_table.add_column("Monthly Cost", justify="right", style="green")

    total_aaas = 0.0
    total_calls = 0
    for agent in aaas_stack:
        aaas_table.add_row(
            agent.name, agent.provider,
            f"~{agent.estimated_calls_per_month:,}",
            f"${agent.monthly_cost:,.2f}"
        )
        total_aaas += agent.monthly_cost
        total_calls += agent.estimated_calls_per_month

    aaas_table.add_section()
    aaas_table.add_row(
        "[bold]TOTAL[/]", "", f"[bold]~{total_calls:,}[/]",
        f"[bold green]${total_aaas:,.2f}/mo[/]"
    )

    # Results
    savings_monthly = total_saas - total_aaas
    savings_pct = (savings_monthly / total_saas) * 100
    savings_annual = savings_monthly * 12

    console.print()
    console.print(saas_table)
    console.print()
    console.print(aaas_table)
    console.print()

    results_panel = Panel(
        f"[bold]Monthly savings:[/] [green]${savings_monthly:,.2f}[/] "
        f"([green]{savings_pct:.1f}% reduction[/])\n"
        f"[bold]Annual savings:[/]  [green]${savings_annual:,.2f}[/]\n"
        f"[bold]Seats eliminated:[/] {total_seats} → 0\n"
        f"[bold]Tasks automated:[/] ~{total_calls:,}/month",
        title="[bold cyan]RESULTS[/]",
        border_style="green",
    )
    console.print(results_panel)

    return {
        "total_saas_monthly": total_saas,
        "total_aaas_monthly": total_aaas,
        "savings_monthly": savings_monthly,
        "savings_annual": savings_annual,
        "savings_pct": savings_pct,
        "seats_eliminated": total_seats,
        "tasks_automated_monthly": total_calls,
    }


if __name__ == "__main__":
    results = run_comparison()
    print(f"\n✓ Cost analysis complete. Savings: {results['savings_pct']:.1f}%")
