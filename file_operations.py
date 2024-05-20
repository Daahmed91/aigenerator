import os
import json
from rich.console import Console
from rich.panel import Panel

console = Console()

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def create_folder_structure(project_name, folder_structure, code_blocks):
    try:
        os.makedirs(project_name, exist_ok=True)
        console.print(Panel(f"Created project folder: [bold]{project_name}[/bold]", title="[bold green]Project Folder[/bold green]", title_align="left", border_style="green"))
    except OSError as e:
        console.print(Panel(f"Error creating project folder: [bold]{project_name}[/bold]\nError: {e}", title="[bold red]Project Folder Creation Error[/bold red]", title_align="left", border_style="red"))
        return

    create_folders_and_files(project_name, folder_structure, code_blocks)

def create_folders_and_files(current_path, structure, code_blocks):
    console.print(f"Creating files and folders in: {current_path}")
    console.print(f"Folder Structure: {json.dumps(structure, indent=2)}")
    console.print(f"Code Blocks: {code_blocks}")

    for key, value in structure.items():
        path = os.path.join(current_path, key)  # Construct the full path
        if isinstance(value, dict):
            try:
                console.print(f"Creating folder at path: {path}")
                os.makedirs(path, exist_ok=True)
                console.print(Panel(f"Created folder: [bold]{path}[/bold]", title="[bold blue]Folder Creation[/bold blue]", title_align="left", border_style="blue"))
                create_folders_and_files(path, value, code_blocks)  # Recursively create subfolders and files
            except OSError as e:
                console.print(Panel(f"Error creating folder: [bold]{path}[/bold]\nError: {e}", title="[bold red]Folder Creation Error[/bold red]", title_align="left", border_style="red"))
        else:
            console.print(f"Looking for code content for file: {key}")
            code_content = next((code for file, code in code_blocks if file == key), None)
            if code_content:
                console.print(f"Creating file at path: {path} with content: {code_content[:50]}...")
                try:
                    with open(path, 'w') as file:
                        file.write(code_content)
                    console.print(Panel(f"Created file: [bold]{path}[/bold]", title="[bold green]File Creation[/bold green]", title_align="left", border_style="green"))
                except IOError as e:
                    console.print(Panel(f"Error creating file: [bold]{path}[/bold]\nError: {e}", title="[bold red]File Creation Error[/bold red]", title_align="left", border_style="red"))
            else:
                console.print(Panel(f"Code content not found for file: [bold]{key}[/bold]", title="[bold yellow]Missing Code Content[/bold yellow]", title_align="left", border_style="yellow"))
