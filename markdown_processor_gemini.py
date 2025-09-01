#!/usr/bin/env python3
"""
Markdown Processing Pipeline with Gemini 2.5 Pro
Reads .md files from input/, processes them with Gemini API, and saves structured output to outputs/
"""

import os
import glob
import json
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

# RAG-Optimized Template for Library Components
TEMPLATE_PROMPT = """
You are a technical documentation formatter specializing in creating RAG-optimized content for library components.

Your task is to reorganize the provided content into a structured template while preserving ALL original information, code examples, and technical details.

Please format the content using this exact structure:

## Metadata
```json
{{
  "library": "[library/framework name - e.g., sera-ui, react-three-fiber, three.js]",
  "component_name": "[main component name]",
  "category": "[category - e.g., forms, animation, ui, visualization, effects]",
  "type": "[type - e.g., react, function, class, hook, utility, shader]",
  "features": ["[feature1]", "[feature2]", "[feature3]"]
}}
```

# Component Name
[Extract the main component/library name from the content]

# Library/Framework
[Identify the primary framework - React, Three.js, Vue, etc.]

# Component Type
[Specify: React Component, Function, Class, Hook, Utility, etc.]

# Core Purpose
[Brief, clear description of what this component does]

# Installation
[Include all npm/yarn install commands and setup instructions from the original]

# Syntax & Parameters
[Document all props, parameters, configuration options, and their types]

# Code Examples
[Include ALL code examples from the original content - preserve every implementation variant]

# Variations & Tweaks
[Document different implementations, styling options, configuration variants shown in the original]

# Common Patterns
[Implementation patterns, best practices, and usage approaches demonstrated]

# Related Components
[Dependencies, related imports, and components that work together]

# Additional Notes
[Any other technical details, comments, troubleshooting, or important information]

# RAG Keywords
[Extract key technical terms for search: component names, framework terms, concepts, methods]

Important guidelines:
- Extract accurate metadata from the content and place it at the very top
- Preserve ALL original code blocks exactly as written
- Maintain ALL examples and implementation variants
- Keep ALL technical details and parameters
- Do not summarize or condense the content
- Only reorganize and categorize the existing information
- Ensure the formatted output contains the same amount of information as the input

Original content to format:

{content}
"""

def setup_gemini():
    """Setup Gemini API client."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        console.print(Panel(
            "[red]GEMINI_API_KEY not found in environment variables.\n"
            "Please create a .env file with:\n"
            "GEMINI_API_KEY=your_api_key_here[/red]",
            title="❌ API Key Missing",
            border_style="red"
        ))
        return None
    
    genai.configure(api_key=api_key)
    
    # Configure the model
    generation_config = {
        "temperature": 0.1,  # Low temperature for consistent formatting
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 32768,  # Gemini 2.5 Pro higher limit
    }
    
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel(
        model_name="models/gemini-2.5-pro",  # Gemini 2.5 Pro with larger context
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    
    return model

def load_markdown(file_path):
    """Load markdown content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        console.print(f"[red]Error reading {file_path}: {e}[/red]")
        return None

def process_with_gemini(text, template, model):
    """Process text with Gemini API."""
    try:
        # Prepare the prompt
        full_prompt = template.format(content=text)
        
        # Call Gemini API
        response = model.generate_content(full_prompt)
        
        if response.text:
            # Check if response was truncated
            response_text = response.text.strip()
            if len(response_text) < len(text) * 0.8:  # If output is significantly smaller
                console.print(f"[yellow]Warning: Response may be truncated (input: {len(text)} chars, output: {len(response_text)} chars)[/yellow]")
            return response_text
        else:
            console.print(f"[red]Gemini returned empty response[/red]")
            if hasattr(response, 'prompt_feedback'):
                console.print(f"[red]Prompt feedback: {response.prompt_feedback}[/red]")
            return None
            
    except Exception as e:
        console.print(f"[red]Error calling Gemini API: {e}[/red]")
        return None

def save_output(content, output_path):
    """Save processed content to output file."""
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        console.print(f"[red]Error saving {output_path}: {e}[/red]")
        return False

def process_markdown_files():
    """Main processing function."""
    start_time = time.time()
    
    # Setup Gemini
    model = setup_gemini()
    if not model:
        return
    
    # Ensure directories exist
    input_dir = "input"
    output_dir = "outputs"
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all markdown files
    files = glob.glob(os.path.join(input_dir, "*.md"))
    
    if not files:
        console.print(Panel(
            "[yellow]No .md files found in input/ directory[/yellow]",
            title="⚠️  Warning",
            border_style="yellow"
        ))
        return
    
    console.print(Panel(
        f"[green]Found {len(files)} markdown files to process[/green]",
        title="🚀 Starting Processing",
        border_style="green"
    ))
    
    # Statistics
    processed = 0
    failed = 0
    processing_times = []
    
    # Process each file
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        for file_path in files:
            filename = os.path.basename(file_path)
            task = progress.add_task(f"Processing {filename}...", total=None)
            file_start_time = time.time()
            
            try:
                # Load markdown content
                raw_content = load_markdown(file_path)
                if raw_content is None:
                    failed += 1
                    continue
                
                # Process with Gemini
                formatted_content = process_with_gemini(raw_content, TEMPLATE_PROMPT, model)
                if formatted_content is None:
                    failed += 1
                    continue
                
                # Save output with same filename
                input_filename = os.path.basename(file_path)
                output_path = os.path.join("outputs", input_filename)
                if save_output(formatted_content, output_path):
                    file_time = time.time() - file_start_time
                    processing_times.append(file_time)
                    processed += 1
                    console.print(f"[green]✅ Processed: {filename} ({file_time:.2f}s)[/green]")
                else:
                    failed += 1
                    
            except Exception as e:
                console.print(f"[red]❌ Failed to process {filename}: {e}[/red]")
                failed += 1
            
            progress.remove_task(task)
    
    total_time = time.time() - start_time
    avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    # Show results
    table = Table(title="Processing Results")
    table.add_column("Status", style="cyan")
    table.add_column("Count", justify="right", style="magenta")
    table.add_column("Time", justify="right", style="yellow")
    
    table.add_row("✅ Successfully Processed", str(processed), f"{avg_time:.2f}s avg")
    table.add_row("❌ Failed", str(failed), "-")
    table.add_row("📁 Total Files", str(len(files)), f"{total_time:.2f}s total")
    
    console.print(table)
    
    if processed > 0:
        console.print(Panel(
            f"[green]Processing complete! Check the outputs/ directory for results.\n\n"
            f"⏱️  Total time: {total_time:.2f} seconds\n"
            f"📊 Average per file: {avg_time:.2f} seconds\n"
            f"🚀 Processing rate: {processed/total_time:.2f} files/second[/green]",
            title="🎉 Success",
            border_style="green"
        ))

def main():
    """Main entry point."""
    console.print(Panel(
        "[bold blue]Markdown Processing Pipeline with Gemini 2.5 Pro[/bold blue]\n"
        "Model: models/gemini-2.5-pro",
        title="📝 Markdown Formatter",
        border_style="blue"
    ))
    
    process_markdown_files()

if __name__ == "__main__":
    main()
