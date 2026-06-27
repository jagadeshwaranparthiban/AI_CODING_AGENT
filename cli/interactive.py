from rich.console import Console
from agents.runner import AgentRunner

console = Console()
runner = AgentRunner()

def start():

    console.print("[bold green]AI Code Agent[/bold green]")
    console.print("Type 'exit' to quit.\n")

    while True:
        prompt = console.input("[cyan]> [/cyan]")
        if prompt.lower() == "exit":
            break

        result = runner.run(prompt)
        console.print(f"\n[green]{result['output']}[/green]\n")