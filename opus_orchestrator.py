import time
import re  # Add this import
from rich.console import Console
from rich.panel import Panel
from groq import Groq
from init import config, client

ORCHESTRATOR_MODEL = config.get("orchestrator_model")
console = Console()

def opus_orchestrator(objective, file_content=None, previous_results=None):
    console.print(f"\n[bold]Calling Orchestrator for your objective[/bold]")
    previous_results_text = "\n".join(previous_results) if previous_results else "None"
    if file_content:
        console.print(Panel(f"File content:\n{file_content}", title="[bold blue]File Content[/bold blue]", title_align="left", border_style="blue"))
    messages = [
        {
            "role": "system",
            "content": "You are an AI orchestrator that breaks down objectives into sub-tasks."
        },
        {
            "role": "user",
            "content": f"Based on the following objective{' and file content' if file_content else ''}, and the previous sub-task results (if any), please break down the objective into the next sub-task, and create a concise and detailed prompt for a subagent so it can execute that task. IMPORTANT!!! when dealing with code tasks make sure you check the code for errors and provide fixes and support as part of the next sub-task. If you find any bugs or have suggestions for better code, please include them in the next sub-task prompt. Please assess if the objective has been fully achieved. If the previous sub-task results comprehensively address all aspects of the objective, include the phrase 'The task is complete:' at the beginning of your response. If the objective is not yet fully achieved, break it down into the next sub-task and create a concise and detailed prompt for a subagent to execute that task.:\n\nObjective: {objective}" + ('\\nFile content:\\n' + file_content if file_content else '') + f"\n\nPrevious sub-task results:\n{previous_results_text}"
        }
    ]

    max_retries = 5
    for attempt in range(max_retries):
        try:
            opus_response = client.chat.completions.create(
                model=ORCHESTRATOR_MODEL,
                messages=messages,
                max_tokens=8000
            )
            response_text = opus_response.choices[0].message.content
            console.print(Panel(response_text, title=f"[bold green]Groq Orchestrator[/bold green]", title_align="left", border_style="green", subtitle="Sending task to Subagent 👇"))
            return response_text, file_content
        except Exception as e:
            if 'rate_limit_exceeded' in str(e):
                retry_after = int(re.findall(r'try again in (\d+)s', str(e))[0])  # Use re.findall here
                console.print(f"[bold red]Rate limit exceeded. Retrying in {retry_after} seconds...[/bold red]")
                time.sleep(retry_after)
            else:
                console.print(f"[bold red]Error during orchestrator processing: {e}[/bold red]")
                raise
    raise Exception("Maximum retries reached for opus_orchestrator")
