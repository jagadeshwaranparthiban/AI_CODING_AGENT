import typer
from rich.console import Console
from agents.runner import AgentRunner
from cli.interactive import start

app = typer.Typer()
console = Console()
runner = AgentRunner()


@app.command()
def generate(prompt: str):
    console.print("[cyan]Running AI Agent...[/cyan]")
    result = runner.run(prompt)

    console.print("[green]Completed[/green]")
    console.print(result["output"])

@app.command()
def chat():
    console.print("[cyan]Starting interactive chat...[/cyan]")
    start()

if __name__ == "__main__":
    app()