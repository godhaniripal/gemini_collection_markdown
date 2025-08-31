#!/usr/bin/env python3
"""
Context Size Analyzer for Markdown Files
Analyzes character count, word count, and estimated token count for markdown files
"""

import os
import glob
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()

def estimate_tokens(text):
    """
    Estimate token count using a simple approximation.
    GPT-style tokenizers typically use ~4 characters per token for English text.
    For code and technical content, it's often closer to 3-3.5 characters per token.
    """
    # Remove extra whitespace and normalize
    cleaned_text = re.sub(r'\s+', ' ', text.strip())
    
    # For technical/code content, use 3.2 chars per token as estimate
    estimated_tokens = len(cleaned_text) / 3.2
    
    return int(estimated_tokens)

def count_code_blocks(text):
    """Count the number of code blocks in the markdown."""
    code_block_pattern = r'```[\s\S]*?```'
    return len(re.findall(code_block_pattern, text))

def analyze_file(file_path):
    """Analyze a single markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stats = {
            'filename': os.path.basename(file_path),
            'file_size_kb': round(os.path.getsize(file_path) / 1024, 2),
            'characters': len(content),
            'characters_no_spaces': len(content.replace(' ', '').replace('\n', '').replace('\t', '')),
            'words': len(content.split()),
            'lines': len(content.splitlines()),
            'code_blocks': count_code_blocks(content),
            'estimated_tokens': estimate_tokens(content)
        }
        
        return stats, content
    
    except Exception as e:
        console.print(f"[red]Error analyzing {file_path}: {e}[/red]")
        return None, None

def get_model_context_limits():
    """Return context limits for popular models."""
    return {
        'llama3.1:8b': 128000,
        'llama3.1:70b': 128000,
        'qwen2.5:14b': 32768,
        'mistral-nemo:12b': 128000,
        'phi3.5:3.8b': 128000,
        'gemma2:9b': 8192,
        'codellama:13b': 16384,
    }

def analyze_directory(directory):
    """Analyze all markdown files in a directory."""
    files = glob.glob(os.path.join(directory, "*.md"))
    
    if not files:
        console.print(f"[yellow]No .md files found in {directory}/[/yellow]")
        return
    
    console.print(Panel(
        f"[blue]Analyzing {len(files)} markdown files in {directory}/[/blue]",
        title="📊 Context Size Analysis",
        border_style="blue"
    ))
    
    # Create results table
    table = Table(title=f"File Analysis Results")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Size (KB)", justify="right", style="magenta")
    table.add_column("Characters", justify="right", style="green")
    table.add_column("Words", justify="right", style="yellow")
    table.add_column("Lines", justify="right", style="blue")
    table.add_column("Code Blocks", justify="right", style="red")
    table.add_column("Est. Tokens", justify="right", style="bold green")
    table.add_column("Model Fit", justify="center", style="white")
    
    total_stats = {
        'files': 0,
        'total_size': 0,
        'total_chars': 0,
        'total_words': 0,
        'total_lines': 0,
        'total_code_blocks': 0,
        'total_tokens': 0
    }
    
    model_limits = get_model_context_limits()
    
    # Analyze each file
    for file_path in files:
        stats, content = analyze_file(file_path)
        if stats is None:
            continue
        
        # Determine which models can handle this file
        model_fit = []
        for model, limit in model_limits.items():
            if stats['estimated_tokens'] <= limit * 0.7:  # Use 70% of context for safety
                model_fit.append("✅")
                break
            elif stats['estimated_tokens'] <= limit * 0.9:  # 90% is risky but possible
                model_fit.append("⚠️")
                break
        else:
            model_fit.append("❌")  # Too large for most models
        
        table.add_row(
            stats['filename'][:20] + ("..." if len(stats['filename']) > 20 else ""),
            str(stats['file_size_kb']),
            f"{stats['characters']:,}",
            f"{stats['words']:,}",
            str(stats['lines']),
            str(stats['code_blocks']),
            f"{stats['estimated_tokens']:,}",
            "".join(model_fit)
        )
        
        # Update totals
        total_stats['files'] += 1
        total_stats['total_size'] += stats['file_size_kb']
        total_stats['total_chars'] += stats['characters']
        total_stats['total_words'] += stats['words']
        total_stats['total_lines'] += stats['lines']
        total_stats['total_code_blocks'] += stats['code_blocks']
        total_stats['total_tokens'] += stats['estimated_tokens']
    
    console.print(table)
    
    # Show totals
    totals_table = Table(title="Summary Statistics")
    totals_table.add_column("Metric", style="cyan")
    totals_table.add_column("Total", justify="right", style="green")
    totals_table.add_column("Average", justify="right", style="yellow")
    
    if total_stats['files'] > 0:
        totals_table.add_row("Files", str(total_stats['files']), "-")
        totals_table.add_row("Size (KB)", f"{total_stats['total_size']:.2f}", f"{total_stats['total_size']/total_stats['files']:.2f}")
        totals_table.add_row("Characters", f"{total_stats['total_chars']:,}", f"{total_stats['total_chars']//total_stats['files']:,}")
        totals_table.add_row("Words", f"{total_stats['total_words']:,}", f"{total_stats['total_words']//total_stats['files']:,}")
        totals_table.add_row("Lines", f"{total_stats['total_lines']:,}", f"{total_stats['total_lines']//total_stats['files']:,}")
        totals_table.add_row("Code Blocks", str(total_stats['total_code_blocks']), f"{total_stats['total_code_blocks']/total_stats['files']:.1f}")
        totals_table.add_row("Est. Tokens", f"{total_stats['total_tokens']:,}", f"{total_stats['total_tokens']//total_stats['files']:,}")
    
    console.print(totals_table)
    
    # Model recommendations
    console.print(Panel(
        "[bold]Model Recommendations:[/bold]\n"
        "✅ = Fits comfortably (< 70% context)\n"
        "⚠️ = Fits but tight (70-90% context)\n" 
        "❌ = Too large (> 90% context)\n\n"
        "[green]Recommended models for your content:[/green]\n"
        "• [bold]qwen2.5:14b[/bold] - Best for instruction following\n"
        "• [bold]llama3.1:70b[/bold] - Best quality (if you have RAM)\n"
        "• [bold]mistral-nemo:12b[/bold] - Good balance\n"
        "• [bold]phi3.5:3.8b[/bold] - Fastest/lightweight",
        title="🎯 Model Selection Guide",
        border_style="green"
    ))

def main():
    """Main entry point."""
    console.print(Panel(
        "[bold blue]Markdown Context Size Analyzer[/bold blue]\n"
        "Analyzes character count, word count, and estimated tokens for RAG processing",
        title="📏 Context Analyzer",
        border_style="blue"
    ))
    
    # Analyze input directory
    if os.path.exists("input"):
        analyze_directory("input")
    else:
        console.print("[red]Input directory not found![/red]")
    
    console.print("\n")
    
    # Also analyze outputs if they exist
    if os.path.exists("outputs"):
        console.print(Panel("[yellow]Output Directory Analysis[/yellow]", border_style="yellow"))
        analyze_directory("outputs")

if __name__ == "__main__":
    main()
