# AI-Driven Application Generator

This project is an AI-driven application generator designed to break down objectives into subtasks and generate code files based on user input. It leverages language models to automate the process, ensuring efficient and accurate code generation. The project employs a master orchestrator to define tasks and subagents to execute them, creating a seamless workflow for complex programming tasks.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Setup](#setup)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

The AI-Driven Application Generator automates the process of breaking down complex programming tasks into smaller, manageable subtasks and generating the corresponding code files. This project ensures that all generated code is saved reliably and that the overall process is efficient.

## Features

- **Task Orchestration**: The master orchestrator breaks down complex objectives into smaller subtasks.
- **Subtask Delegation**: Subagents handle the execution of each subtask.
- **Error Handling**: Detailed error handling and logging for robust execution.
- **File Management**: Reliable file handling and project structure creation.
- **Checkpointing**: Saves progress to prevent data loss in case of interruptions.

## How It Works

The AI-Driven Application Generator uses two main components: the master orchestrator and the subagents.

### Master Orchestrator

The master orchestrator is responsible for:

1. **Receiving Objectives**: It takes user input specifying the objective.
2. **Breaking Down Tasks**: It divides the objective into smaller, manageable subtasks.
3. **Reviewing Outputs**: It reviews the outputs from subagents to ensure they meet the specified requirements.

### Subagents

Subagents are responsible for:

1. **Executing Subtasks**: They perform the tasks defined by the master orchestrator.
2. **Generating Code**: They create the necessary code files based on the task requirements.
3. **Handling Errors**: They provide feedback on any issues encountered during execution.

### Workflow

1. **Initialization**: The user inputs an objective and any associated files.
2. **Task Breakdown**: The orchestrator breaks the objective into subtasks.
3. **Subtask Execution**: Subagents execute the subtasks and generate code.
4. **Review and Refine**: The orchestrator reviews the outputs and refines them if necessary.
5. **File Creation**: The project structure and files are created and saved.

## Setup

### Prerequisites

- Python 3.7 or higher
- Required Python packages (see `requirements.txt`)

### Set up 

1. Open Config,json file and input your grok api. 
2. Run main.py file
3. Input your objective  
