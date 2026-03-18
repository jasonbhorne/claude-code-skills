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

**2c. Scan for media companion reports**
Search `~/Documents/Research/` for companion guide .docx files dated within the week range:
- Filename pattern: files containing "Companion Guide" in the name, with a date prefix matching the week (e.g., `2026-03-18 DTF St. Louis Companion Guide.docx`)
- Also check Obsidian session logs tagged `media-companion` for metadata (title, media type, spoiler tier, quick take, recommendations)
- For each report found, extract: title, media type (book/show/movie), a condensed no-spoiler quick take (2-3 sentences), and up to 3-4 recommendation titles

**2d. Query NotebookLM API**
Run `notebooklm list --json` to get all notebooks with creation dates. Filter to notebooks created within the week range. For each matching notebook:
- Note the title and creation date
- Check if this notebook was already captured in an Obsidian session log (to avoid duplicates). If a Claude Code session created the notebook, it's already covered. Tag it with the NotebookLM badge only if it was direct browser usage or if the primary value was the NotebookLM interaction (e.g., podcast generation, interactive Q&A).
- Categorize based on the notebook title

**2e. Combine and categorize**
Group all AI usage into categories:
- **District Operations:** HR, finance, enrollment, data analysis, board prep, compliance
- **Teaching & Academic:** Course materials, dissertation reviews, paper grading, student feedback
- **Research & Writing:** Deep research, blog posts, reports, documents
- **Website & Social:** Site reviews, blog publishing, SEO, analytics
- **Code & Automation:** Skills, scripts, pipelines, GitHub
- **Personal:** Health tracking, shopping, home projects, fantasy football
- **What I'm Into:** Media companion guides generated this week (books, shows, movies). This section renders differently from other categories (see HTML structure below). Only include if media companion reports were found in step 2c.

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
- Media companion guides: ~4-6h per guide
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
    .ai-week .media-card { padding: 14px 0; border-bottom: 1px solid #f0f0f0; }
    .ai-week .media-card:last-child { border-bottom: none; }
    .ai-week .media-title { font-size: 1em; font-weight: 600; color: #1a1a1a; }
    .ai-week .media-type { display: inline-block; font-size: 0.7em; font-weight: 600; padding: 2px 8px; border-radius: 12px; margin-left: 8px; }
    .ai-week .media-type.book { background: #fff3cd; color: #856404; }
    .ai-week .media-type.show { background: #d1ecf1; color: #0c5460; }
    .ai-week .media-type.movie { background: #f8d7da; color: #721c24; }
    .ai-week .media-take { font-size: 0.88em; color: #555; line-height: 1.5; margin: 6px 0; }
    .ai-week .media-recs { font-size: 0.8em; color: #888; }
    .ai-week .media-recs strong { color: #666; font-weight: 600; }
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

  <!-- "What I'm Into" section (only if media companion reports exist for the week) -->
  <!-- This section appears LAST, just before the stats footer -->
  <h2>What I'm Into</h2>
  <div>
    <div class="media-card">
      <div>
        <span class="media-title">{Title}</span>
        <span class="media-type show">TV Show</span>
        <!-- Use class "book" for books, "show" for TV, "movie" for movies -->
        <!-- Label text: "Book", "TV Show", or "Movie" -->
      </div>
      <div class="media-take">{Condensed no-spoiler take, 2-3 sentences max}</div>
      <div class="media-recs"><strong>If you liked this:</strong> {Rec 1}, {Rec 2}, {Rec 3}</div>
    </div>
    <!-- Repeat for each media companion report found -->
  </div>

  <!-- Summary stats at bottom -->
  <div class="stats">
    <span>{total_tasks}</span> tasks across <span>{tool_count}</span> AI tools
    <!-- When media items are present, add this line: -->
    <br>Plus <span>{N}</span> media companion guide(s) generated this week
  </div>
</div>
```

#### "What I'm Into" Content Rules
- The quick take MUST be rewritten as no-spoiler regardless of the original report's spoiler tier
- Keep it to 2-3 sentences: what it is, whether it's worth watching/reading, one interesting detail
- No plot details whatsoever
- Recommendations condensed to title-only (no rationales), comma-separated, max 3-4 items
- Tone matches Jason's blog voice: direct, opinionated, specific
- Sanitize titles for a public school official's blog: when a title could cause confusion or read poorly out of context, prefer a descriptive genre title instead (e.g., "HBO Murder Mystery Mini-Series" not "DTF St. Louis"). Flag anything ambiguous for Jason to review before publishing
- Media type badge: use `.book` for books, `.show` for TV shows, `.movie` for movies
- If no media companion reports exist for the week, omit the entire "What I'm Into" section AND the companion guide line in the stats footer

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
