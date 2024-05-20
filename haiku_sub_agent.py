import time
import re  # Add this import
from rich.console import Console
from rich.panel import Panel
from groq import Groq
from init import config, client

SUB_AGENT_MODEL = config.get("sub_agent_model")
console = Console()

def haiku_sub_agent(prompt, previous_haiku_tasks=None, continuation=False):
    previous_haiku_tasks = previous_haiku_tasks or []

    continuation_prompt = "Continuing from the previous answer, please complete the response."
    system_message = "Previous Haiku tasks:\n" + "\n".join(f"Task: {task['task']}\nResult: {task['result']}" for task in previous_haiku_tasks)
    if continuation:
        prompt = continuation_prompt

    messages = [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    max_retries = 5
    for attempt in range(max_retries):
        try:
            haiku_response = client.chat.completions.create(
                model=SUB_AGENT_MODEL,
                messages=messages,
                max_tokens=8000
            )
            response_text = haiku_response.choices[0].message.content
            console.print(Panel(response_text, title="[bold blue]Groq Sub-agent Result[/bold blue]", title_align="left", border_style="blue", subtitle="Task completed, sending result to Orchestrator 👇"))
            return response_text
        except Exception as e:
            if 'rate_limit_exceeded' in str(e):
                retry_after = int(re.findall(r'try again in (\d+)s', str(e))[0])  # Use re.findall here
                console.print(f"[bold red]Rate limit exceeded. Retrying in {retry_after} seconds...[/bold red]")
                time.sleep(retry_after)
            else:
                console.print(f"[bold red]Error during sub-agent processing: {e}[/bold red]")
                raise
    raise Exception("Maximum retries reached for haiku_sub_agent")
