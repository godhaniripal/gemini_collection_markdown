# Markdown Processor with Ollama - RAG Optimized

A Python pipeline that processes markdown files using Ollama's llama3.1:8b model to format them into a RAG-optimized template for library components and their variations.

## Prerequisites

1. **Ollama installed** - Download from [ollama.ai](https://ollama.ai)
2. **llama3.1:8b model** - Install with: `ollama pull llama3.1:8b`
3. **Python packages** - Install with: `pip install -r requirements.txt`

## Structure

```
├── input/          # Place your raw .md files here
├── outputs/        # Formatted files will be saved here (same filenames)
├── markdown_processor.py  # Main script
└── requirements.txt
```

## Usage

1. Place your raw markdown files in the `input/` directory
2. Run the processor:
   ```bash
   python markdown_processor.py
   ```
3. Check the `outputs/` directory for formatted results (same filenames as input)

## RAG-Optimized Template Format

The script formats all markdown files into this structure optimized for RAG systems:

- **Component Name** - Clear component identifier
- **Library/Framework** - Parent library name
- **Component Type** - Function, Class, Method, etc.
- **Core Purpose** - One-sentence description
- **Syntax & Parameters** - Detailed syntax with types
- **Code Examples** - Multiple practical examples
- **Variations & Tweaks** - Different usage patterns and configurations
- **Common Patterns** - Best practices and typical implementations
- **Related Components** - Components that work together
- **Troubleshooting** - Common issues and solutions
- **RAG Keywords** - Search terms for retrieval

## Perfect For

- 📚 Library documentation processing
- 🔍 RAG system data preparation
- 📖 Component variation documentation
- 🛠️ Technical reference creation

## Features

- ✅ Beautiful terminal interface with Rich
- ✅ Progress tracking
- ✅ Error handling and logging
- ✅ Modular function design
- ✅ Automatic directory creation
- ✅ Processing statistics

## Functions

- `load_markdown(file)` - Loads markdown content
- `process_with_ollama(text, template)` - Processes with Ollama
- `save_output(content, out_file)` - Saves formatted output
