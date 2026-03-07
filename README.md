# Claude Code Skills Library

A collection of reusable [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for education administration, document processing, research, and productivity automation.

These skills extend Claude Code with specialized capabilities through `SKILL.md` files placed in `~/.claude/skills/<skill-name>/`.

## Skills

### Document Review & Feedback

| Skill | Description |
|-------|-------------|
| [doc-review](skills/doc-review/) | Review any `.docx` file and insert Word comments for typos, errors, formatting issues, and other feedback |
| [dissertator](skills/dissertator/) | Review a dissertation and insert Word comments with rigorous, constructive feedback. Covers APA 7, university template requirements, and chapter-specific analysis |
| [ai-paper-review](skills/ai-paper-review/) | Review a student's AI leadership paper and insert Word comments with rubric-based feedback |

### Content Generation

| Skill | Description |
|-------|-------------|
| [pptx](skills/pptx/) | Generate a professional PowerPoint presentation from a folder of source documents and a prompt. Includes a complete slide type library with branded styling |
| [newsletter](skills/newsletter/) | Generate a monthly AI newsletter with web research, archive cross-checking, and multi-agent content discovery |
| [newsletter-link](skills/newsletter-link/) | Quick-add a link to the must-include list for the next newsletter |
| [notes-cleanup](skills/notes-cleanup/) | Clean up rough notes (meetings, voice memos, brainstorming) into polished, structured text |
| [notebooklm](skills/notebooklm/) | Full programmatic access to Google NotebookLM via CLI. Create notebooks, add sources, generate podcasts, slide decks, quizzes, and more |
| [notebooklm-pipeline](skills/notebooklm-pipeline/) | Automated NotebookLM pipeline: create notebook, add sources, then generate podcast + report + quiz + slides in parallel |

### Productivity & Operations

| Skill | Description |
|-------|-------------|
| [time-savings](skills/time-savings/) | Generate a Time Savings Tracker spreadsheet (.xlsx) with a Task Log and Summary dashboard |
| [check-in](skills/check-in/) | Clean up Friday leadership check-in notes into polished DOCX/PDF files and maintain an action item tracker |
| [weekly-ops](skills/weekly-ops/) | Autonomously run recurring workflows based on the current date, pass context between tasks, and produce a Weekly Briefing document |
| [organize-folder](skills/organize-folder/) | Create a folder organizer script and clickable `.command` file for any directory |
| [financial-advisor](skills/financial-advisor/) | Monthly personal financial analysis with XLSX dashboard and DOCX narrative report using 4 parallel agents |

### Calendar & Scheduling

| Skill | Description |
|-------|-------------|
| [new_calendar](skills/new_calendar/) | Shift a school calendar Excel file to the next school year, preserving all formatting. Uses XML manipulation to avoid openpyxl font bugs |

### Meta

| Skill | Description |
|-------|-------------|
| [create-skill](skills/create-skill/) | Autonomously build, test, and validate a new Claude Code skill from a natural language description |

## Installation

Copy any skill folder into your Claude Code skills directory:

```bash
# Copy a single skill
cp -r skills/doc-review ~/.claude/skills/

# Copy all skills
cp -r skills/* ~/.claude/skills/
```

Then invoke with `/skill-name` in Claude Code (e.g., `/doc-review path/to/file.docx`).

## Customization

Most skills use placeholder variables that you should customize for your environment:

| Variable | Description | Example |
|----------|-------------|---------|
| `$AUTHOR_NAME` | Your name for document metadata | `Jane Smith` |
| `$AUTHOR_FULL` | Your full name with credentials | `Dr. Jane Smith, Ed.D.` |
| `$AUTHOR_WEBSITE` | Your website domain | `janesmith.com` |
| `$ONEDRIVE_WORK` | Path to your work OneDrive/cloud sync | `~/Library/CloudStorage/OneDrive-MyOrg/` |
| `$ONEDRIVE_PERSONAL` | Path to your personal OneDrive/cloud sync | `~/Library/CloudStorage/OneDrive-Personal/` |
| `$DISTRICT_NAME` | Your organization/district name | `Springfield Schools` |

Find-and-replace these in any skill you install.

## Key Patterns

These skills demonstrate several reusable Claude Code patterns:

- **Word comment insertion** via `python-docx` + `lxml` XML (doc-review, ai-paper-review) or direct ZIP/XML manipulation for Word 2016+ compatibility (dissertator)
- **Agent teams** for parallel processing (newsletter content discovery, dissertation multi-pass review, financial analysis)
- **Self-contained Python generation** where the skill writes a complete Python script to `/tmp/`, executes it, and cleans up (pptx, time-savings, financial-advisor)
- **CLI tool integration** with `notebooklm-py` for NotebookLM automation
- **Shared context files** for multi-task orchestration (weekly-ops)
- **Skill-as-meta-skill** where one skill autonomously creates other skills (create-skill)

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- macOS (some skills use `open` command and AppleScript)
- Python 3 with common packages: `python-docx`, `openpyxl`, `python-pptx`, `lxml`, `PyMuPDF`
- For NotebookLM skills: `pip install notebooklm-py`

## License

MIT
