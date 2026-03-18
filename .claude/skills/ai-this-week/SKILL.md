# AI This Week: $ARGUMENTS

## Description
Generate a Squarespace-ready HTML block summarizing how Jason used AI tools during the week. Reads from a weekly input folder and Obsidian session logs, produces a styled HTML snippet for a Squarespace Code Block.

## Trigger
- `/ai-this-week` or `/ai-this-week March 15-22`
- "generate ai this week", "what did I use AI for this week", "update ai this week"

## Configuration

### Input Sources
1. **Weekly folder:** `~/Documents/AI This Week/{week folder}/`
   - Folder naming: `{Month} {start}-{Month} {end} {year}` (e.g., `March 15-March 22 2026`)
   - Drop any files here: text notes, screenshots, docs, etc. from any AI tool (ChatGPT exports, Gemini, NotebookLM, etc.)
   - The skill reads ALL files in the folder as input context
2. **Obsidian session logs:** `Sessions/` folder in the vault
   - Search for session notes dated within the week's range
   - These capture Claude Code usage automatically

### Output
- **Primary:** HTML file saved to the weekly folder as `ai-this-week.html`
- **Secondary:** The HTML is also printed to terminal for easy copy-paste into Squarespace

## Workflow

### Step 1: Determine the Week

Default: find the most recent weekly folder in `~/Documents/AI This Week/`.

If `$ARGUMENTS` specifies a week (e.g., "March 15-22"), find or create that folder.

Parse the folder name to get `week_start` and `week_end` dates.

### Step 2: Gather Input

**2a. Read the weekly folder**
Read all files in `~/Documents/AI This Week/{week folder}/`. These may include:
- Plain text notes about ChatGPT, Gemini, NotebookLM, or other AI tool usage
- Exported chat logs or screenshots
- Any manual notes Jason dropped in

**2b. Search Obsidian session logs**
Use the Obsidian MCP tools to search for session notes dated within the week range:
- `search_notes` for sessions in the date range
- `read_note` on each matching session to extract: task summary, tools used, outputs created

**2c. Query NotebookLM API**
Run `notebooklm list --json` to get all notebooks with creation dates. Filter to notebooks created within the week range. For each matching notebook:
- Note the title and creation date
- Check if this notebook was already captured in an Obsidian session log (to avoid duplicates). If a Claude Code session created the notebook, it's already covered. Tag it with the NotebookLM badge only if it was direct browser usage or if the primary value was the NotebookLM interaction (e.g., podcast generation, interactive Q&A).
- Categorize based on the notebook title

**2d. Combine and categorize**
Group all AI usage into categories:
- **District Operations:** HR, finance, enrollment, data analysis, board prep, compliance
- **Teaching & Academic:** Course materials, dissertation reviews, paper grading, student feedback
- **Research & Writing:** Deep research, blog posts, reports, documents
- **Website & Social:** Site reviews, blog publishing, SEO, analytics
- **Code & Automation:** Skills, scripts, pipelines, GitHub
- **Personal:** Health tracking, shopping, home projects, fantasy football
For each item, capture:
- What was done (1-2 sentences max)
- Which AI tool(s) were used (Claude Code, ChatGPT, Gemini, NotebookLM, MagicSchool, etc.)
- The output or result (if tangible)
- Estimated time saved vs doing it manually (conservative estimates)

#### Time Saved Guidelines
- Quick lookups/questions: ~10-30m
- Document drafting: ~1-2h
- Research reports (multi-source): ~8-12h per report
- Skill/tool building: ~3-6h per skill
- Deep research with 40+ sources: ~10-15h
- NotebookLM notebook setup with sources: ~30m-1h
- Image generation/visualization: ~30m-1h
- Bug fixes/debugging: ~2-4h
- Blog posts: ~2-3h
Total the estimates and display in the stats footer.

### Step 3: Generate HTML

Produce a self-contained HTML block styled for Squarespace. The design should be:
- Clean, minimal, modern
- Works inside a Squarespace Code Block (no external CSS/JS dependencies)
- All styles inline or in a single `<style>` tag within the block
- Responsive (works on mobile)

#### HTML Structure

```html
<div class="ai-week">
  <style>
    .ai-week { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 720px; margin: 0 auto; }
    .ai-week h2 { font-size: 1.1em; color: #1a1a1a; border-bottom: 2px solid #e5e5e5; padding-bottom: 6px; margin-top: 28px; margin-bottom: 12px; }
    .ai-week .week-date { font-size: 0.9em; color: #666; margin-bottom: 24px; }
    .ai-week ul { list-style: none; padding: 0; margin: 0; }
    .ai-week li { padding: 8px 0; border-bottom: 1px solid #f0f0f0; display: flex; align-items: flex-start; gap: 10px; }
    .ai-week li:last-child { border-bottom: none; }
    .ai-week .tool-badge { display: inline-block; font-size: 0.7em; font-weight: 600; padding: 2px 8px; border-radius: 12px; white-space: nowrap; flex-shrink: 0; margin-top: 2px; }
    .ai-week .claude { background: #f0e6d3; color: #8b6914; }
    .ai-week .chatgpt { background: #d4edda; color: #155724; }
    .ai-week .gemini { background: #cce5ff; color: #004085; }
    .ai-week .notebooklm { background: #e2d9f3; color: #4a235a; }
    .ai-week .magicschool { background: #fce4ec; color: #880e4f; }
    .ai-week .other { background: #e9ecef; color: #495057; }
    .ai-week .task-text { font-size: 0.92em; color: #333; line-height: 1.4; }
    .ai-week .output { font-size: 0.8em; color: #888; font-style: italic; }
    .ai-week .stats { margin-top: 24px; padding: 12px 16px; background: #f8f9fa; border-radius: 8px; font-size: 0.85em; color: #555; }
    .ai-week .stats span { font-weight: 600; color: #1a1a1a; }
    .ai-week .stats .time-total { color: #2e7d32; font-weight: 700; }
    .ai-week .time-saved { font-size: 0.75em; color: #2e7d32; font-weight: 600; margin-left: auto; white-space: nowrap; flex-shrink: 0; }
  </style>

  <div class="week-date">Week of {start_date} - {end_date}, {year}</div>

  <!-- One section per category that has items (omit empty categories) -->
  <h2>{Category Name}</h2>
  <ul>
    <li>
      <span class="tool-badge claude">Claude Code</span>
      <div>
        <div class="task-text">{What was done}</div>
        <div class="output">{Output or result}</div>
      </div>
    </li>
    <!-- more items -->
  </ul>

  <!-- Repeat for each category with items -->

  <!-- Summary stats at bottom -->
  <div class="stats">
    <span>{total_tasks}</span> tasks across <span>{tool_count}</span> AI tools
  </div>
</div>
```

#### Tool Badge Classes
- Claude Code / Claude: `.claude`
- ChatGPT / OpenAI: `.chatgpt`
- Gemini / Google AI: `.gemini`
- NotebookLM: `.notebooklm`
- MagicSchool: `.magicschool`
- Any other tool: `.other`

#### Style Rules
- List format, not paragraphs. Keep each item to 1-2 lines max.
- Tool badge appears to the left of each item for quick scanning
- Output/result line is optional, only include when there's a tangible deliverable (a file, a report, a published post)
- Omit categories that have no items for the week
- No emojis unless Jason specifically adds them to his notes

### Step 4: Save and Display

1. Save the HTML to `~/Documents/AI This Week/{week folder}/ai-this-week.html`
2. Print the full HTML to terminal so Jason can copy-paste into Squarespace
3. Print a brief summary: number of items, categories covered, tools used

### Step 5: Squarespace Instructions

After generating, remind Jason:
1. Go to the "AI This Week" page on jasonhorne.org
2. Add a new **Code Block** (not text block) at the top of the page
3. Paste the HTML
4. Save and publish

Each week's HTML block stacks on the page, newest on top. Previous weeks remain visible below.

## Notes

- If the weekly folder is empty AND no Obsidian sessions are found, tell Jason there's nothing to generate yet
- If only Obsidian sessions exist (no manual additions), generate from those alone, they capture Claude Code usage well
- If only manual files exist (no Obsidian sessions), generate from those alone
- Keep descriptions factual and concise. This is a log, not a narrative.
- Do NOT include confidential items (HR, legal, personnel matters). If a session log is tagged as confidential or mentions sensitive topics, skip it or use a vague description like "Confidential administrative task"
