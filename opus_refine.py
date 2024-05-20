import json
import re  # Add this import
import time  # Add this import
from rich.console import Console
from rich.panel import Panel
from groq import Groq
from init import config, client

REFINER_MODEL = config.get("refiner_model")
console = Console()

def opus_refine(objective, sub_task_results, timestamp, project_name, continuation=False):
    console.print("\nCalling Opus to provide the refined final output for your objective:")
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that refines sub-task results into a cohesive final output."
        },
        {
            "role": "user",
            "content": "Objective: " + objective + "\n\nSub-task results:\n" + "\n".join(sub_task_results) + "\n\nPlease review and refine the sub-task results into a cohesive final output. Add any missing information or details as needed. Make sure the code files are completed. When working on code projects, ONLY AND ONLY IF THE PROJECT IS CLEARLY A CODING ONE please provide the following:\n1. Project Name: Create a concise and appropriate project name that fits the project based on what it's creating. The project name should be no more than 20 characters long.\n2. Folder Structure: Provide the folder structure as a valid JSON object, where each key represents a folder or file, and nested keys represent subfolders. Use null values for files. Ensure the JSON is properly formatted without any syntax errors. Make sure all keys are enclosed in double quotes, and ensure objects are correctly encapsulated with braces, separating items with commas as necessary.\nWrap the JSON object in <folder_structure> tags.\n3. Code Files: For each code file, include ONLY the file name in this format 'Filename: <filename>' NEVER EVER USE THE FILE PATH OR ANY OTHER FORMATTING YOU ONLY USE THE FOLLOWING format 'Filename: <filename>' followed by the code block enclosed in triple backticks, with the language identifier after the opening backticks, like this:\n\n​python\n<code>\n​"
        }
    ]

    max_retries = 5
    for attempt in range(max_retries):
        try:
            opus_response = client.chat.completions.create(
                model=REFINER_MODEL,
                messages=messages,
                max_tokens=8000
            )
            response_text = opus_response.choices[0].message.content
            console.print(Panel(response_text, title="[bold green]Final Output[/bold green]", title_align="left", border_style="green"))
            return response_text
        except Exception as e:
            if 'rate_limit_exceeded' in str(e):
                retry_after = int(re.findall(r'try again in (\d+)s', str(e))[0])
                console.print(f"[bold red]Rate limit exceeded. Retrying in {retry_after} seconds...[/bold red]")
                time.sleep(retry_after)
            else:
                console.print(f"[bold red]Error during refining: {e}[/bold red]")
                raise
    raise Exception("Maximum retries reached for opus_refine")

def extract_json_from_refined_output(refined_output):
    try:
        folder_structure_str = re.search(r'<folder_structure>(.*?)</folder_structure>', refined_output, re.DOTALL).group(1)
        folder_structure = json.loads(folder_structure_str)
        code_blocks = re.findall(r'Filename: (.*?)```(.*?)```', refined_output, re.DOTALL)
        code_blocks = [(filename.strip(), code.strip()) for filename, code in code_blocks]
        return folder_structure, code_blocks
    except Exception as e:
        console.print(f"[bold red]Error parsing refined output as JSON: {e}[/bold red]")
        return None, []
