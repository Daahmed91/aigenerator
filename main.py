import re
import json
import logging
import time
import os  # Add this import to handle file operations
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

# Import custom modules
from file_operations import read_file, create_folder_structure
from opus_orchestrator import opus_orchestrator
from haiku_sub_agent import haiku_sub_agent
from opus_refine import opus_refine, extract_json_from_refined_output
from logging_config import setup_logging
from init import load_config  # Import from the new init module

# Initialize the Rich Console
console = Console()

def get_user_input(prompt):
    try:
        user_input = input(prompt)
        if user_input.lower() in ['quit', 'exit']:
            console.print("[bold red]Exiting the program. Goodbye![/bold red]")
            exit()
        return user_input
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting the program. Goodbye![/bold red]")
        exit()

def save_checkpoint(checkpoint_data, filename='checkpoint.json'):
    with open(filename, 'w') as f:
        json.dump(checkpoint_data, f, indent=2)

def load_checkpoint(filename='checkpoint.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def main():
    setup_logging()
    logging.info("Application started.")
    
    try:
        config = load_config()
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        console.print(f"[bold red]Error loading configuration: {e}[/bold red]")
        return
    
    console.print("Welcome to the AI-driven application generator!", style="bold underline")
    console.print("Please enter your objective in the format: 'Develop a Python script that ...'")
    console.print("If your objective includes a file, please include the file path.")
    
    objective = get_user_input("Enter your objective (or type 'quit' to exit): ")

    file_content = None
    try:
        if "./" in objective or "/" in objective:
            file_path = re.findall(r'[./\w]+\.[\w]+', objective)[0]
            file_content = read_file(file_path)
            objective = objective.split(file_path)[0].strip()
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        return

    max_retries = 5
    retry_delay = 10  # Delay between retries in seconds

    checkpoint_data = load_checkpoint()
    if checkpoint_data:
        objective = checkpoint_data.get('objective', objective)
        task_exchanges = checkpoint_data.get('task_exchanges', [])
        haiku_tasks = checkpoint_data.get('haiku_tasks', [])
        previous_results = checkpoint_data.get('previous_results', [])
        project_name = checkpoint_data.get('project_name', config.get("project_name", "AI_Driven_Application"))
    else:
        task_exchanges = []
        haiku_tasks = []
        previous_results = []
        project_name = config.get("project_name", "AI_Driven_Application")

    for attempt in range(max_retries):
        try:
            while True:
                previous_results = [result for _, result in task_exchanges]

                try:
                    if not task_exchanges:
                        opus_result, file_content_for_haiku = opus_orchestrator(objective, file_content, previous_results)
                    else:
                        opus_result, _ = opus_orchestrator(objective, previous_results=previous_results)

                    console.print(f"[bold yellow]Orchestrator Result:[/bold yellow]\n{opus_result}")

                    if "The task is complete:" in opus_result:
                        final_output = opus_result.replace("The task is complete:", "").strip()
                        break
                    else:
                        sub_task_prompt = opus_result
                        if file_content_for_haiku and not haiku_tasks:
                            sub_task_prompt += f"\n\nFile content:\n{file_content_for_haiku}"
                        sub_task_result = haiku_sub_agent(sub_task_prompt, haiku_tasks)
                        haiku_tasks.append({"task": sub_task_prompt, "result": sub_task_result})
                        task_exchanges.append((sub_task_prompt, sub_task_result))
                        file_content_for_haiku = None

                        # Save checkpoint after each successful sub-task
                        checkpoint_data = {
                            'objective': objective,
                            'task_exchanges': task_exchanges,
                            'haiku_tasks': haiku_tasks,
                            'previous_results': previous_results,
                            'project_name': project_name
                        }
                        save_checkpoint(checkpoint_data)
                except Exception as e:
                    logging.error(f"Error during task processing: {e}")
                    console.print(f"[bold red]Error during task processing: {e}[/bold red]")
                    raise

            sanitized_objective = re.sub(r'\W+', '_', objective)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            try:
                # Process the collected results and generate final output
                refined_output = opus_refine(objective, [result for _, result in task_exchanges], timestamp, project_name)

                console.print(f"[bold yellow]Refined Output:[/bold yellow]\n{refined_output}")

                # Extract JSON from refined output
                folder_structure, code_blocks = extract_json_from_refined_output(refined_output)

                if folder_structure is None or not code_blocks:
                    console.print("[bold red]Failed to extract necessary data from refined output.[/bold red]")
                    logging.error("Failed to extract necessary data from refined output.")
                    raise ValueError("Failed to extract necessary data from refined output.")

                console.print(f"[bold yellow]Folder Structure:[/bold yellow]\n{json.dumps(folder_structure, indent=2)}")
                console.print(f"[bold yellow]Code Blocks:[/bold yellow]\n{code_blocks}")

                create_folder_structure(project_name, folder_structure, code_blocks)

                filename = f"{timestamp}_{sanitized_objective[:25]}.md"  # Ensure filename is not too long
                with open(filename, 'w') as file:
                    file.write(f"Objective: {objective}\n\n")
                    file.write("=" * 40 + " Task Breakdown " + "=" * 40 + "\n\n")
                    for i, (prompt, result) in enumerate(task_exchanges, start=1):
                        file.write(f"Task {i}:\nPrompt: {prompt}\nResult: {result}\n\n")
                    file.write("=" * 40 + " Refined Final Output " + "=" * 40 + "\n\n")
                    file.write(refined_output)

                console.print(f"\n[bold]Refined Final output:[/bold]\n{refined_output}")
                console.print(f"\nFull exchange log saved to {filename}")
                logging.info(f"Full exchange log saved to {filename}")

                # Remove checkpoint file after successful completion
                if os.path.exists('checkpoint.json'):
                    os.remove('checkpoint.json')
                break  # Exit the retry loop if successful
            except Exception as e:
                logging.error(f"Error during final output processing: {e}")
                console.print(f"[bold red]Error during final output processing: {e}[/bold red]")
                raise

        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            console.print(f"[bold red]Attempt {attempt + 1} failed: {e}[/bold red]")
            if attempt < max_retries - 1:
                console.print(f"[bold red]Retrying in {retry_delay} seconds...[/bold red]")
                time.sleep(retry_delay)
            else:
                console.print("[bold red]Maximum retries reached. Exiting...[/bold red]")
                logging.error("Maximum retries reached. Exiting...")
                break

if __name__ == "__main__":
    main()
