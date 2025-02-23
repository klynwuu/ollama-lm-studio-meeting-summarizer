# Meeting Summarizer

An automated meeting summarization tool that processes transcript files and generates AI-powered summaries using large language models.

## Features
- 🕒 Automatically detects latest transcript file in target folder
- 🤖 Supports multiple LLM backends via OpenAI-compatible API
- 📝 Processes .txt, .srt, and .md file formats
- 📊 Generates both clean summaries and detailed processing logs
- ⚙️ Configurable via environment variables and prompt templates

## Workflow Diagram

```mermaid
flowchart LR
    A[Load Environment Variables] --> B[Load Prompt Templates]
    B --> C[Find Latest Transcript]
    C --> D[Call LLM Server]
    D --> E[Process Response]
    E --> F[Generate Summary.md]
    E --> G[Generate Log File]
```

## Installation

```bash

```

## Configuration

1. Create `.env` file with these variables:
```ini
API_KEY=your_api_key
LLM_SERVER_BASE_URL=https://your-llm-provider.com/v1
LLM_MODEL=your-model-name
TEMPERATURE=0.7
TARGET_FOLDER=folder-with-transcripts
```

2. Set up prompt templates in `prompts/` directory:
```yaml
# system_prompts.yaml
system_prompt_meeting_summarizer: |
  You are an expert meeting summarizer...
```

## Usage

1. Place transcript files in the `TARGET_FOLDER` (default: ./transcripts)
2. Run the summarizer:
```bash
python meeting_summarizer_v1.py
```

## Output Files
- `[FILENAME]_summary.md`: Clean meeting summary
- `[FILENAME].log`: Full processing log including raw LLM response

## Supported File Formats
- Text files (.txt)
- Subtitle files (.srt)
- Markdown files (.md)

## Dependencies
- Python 3.8+
- See `requirements.txt` for package dependencies


Key components explained in the Mermaid diagram:

1. **Environment Setup**: Loads config from `.env` and prompt templates
2. **Transcript Handling**: Finds latest compatible file in target folder
3. **LLM Processing**: Sends structured prompt to language model
4. **Output Generation**: Creates cleaned summary and detailed log files

The diagram shows the linear workflow from configuration loading through to final output generation, highlighting the key stages of the summarization process.