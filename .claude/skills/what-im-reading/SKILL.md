# What I'm Reading

## Description
Generate a Squarespace-ready HTML block showing Jason's current Audible reading list. Pulls live data from the Audible library, sorts by purchase date (most recent first as a proxy for start date), and produces styled book cards with a brief take on each title.

## Trigger
- `/what-im-reading`
- "what am I reading", "reading list", "update reading", "current reads", "what I'm reading"

## Configuration

### Audible credentials
- Credentials file: `~/.config/audible/credentials.json`
- The script auto-refreshes the access token when expired. No manual intervention needed.

### Script
`~/Scripts/audible_listening.py` with `--sort recent` flag (sorts by purchase_date descending).

### Output
- HTML file: `~/Documents/What Im Reading/what-im-reading.html`
- Also printed to terminal for copy-paste into Squarespace

## Workflow

### Step 1: Pull Audible data

Run:
```
/opt/anaconda3/bin/python3 ~/Scripts/audible_listening.py --sort recent
```

This returns JSON with all books that have any listening progress (percent_complete > 0), sorted by purchase_date descending (most recent purchase first). The `is_finished` flag is unreliable, so include all books with any progress.

### Step 2: Generate brief takes

For each book in the list, write a 1-2 sentence take in Jason's voice:
- Direct and opinionated. Say what it is and whether it's worth the time.
- Specific details over vague praise ("good pacing" is useless; "the author spends too long on X" is useful).
- No hedging. No "I found this interesting." Just the take.
- Keep it punchy. These are captions, not reviews.

If you don't have enough context to write a real take from the title and author alone, write a neutral placeholder like: "Just started this one." or "Still early, but the premise is [X]."

### Step 3: Generate HTML

Produce a self-contained HTML block styled for Squarespace. Inline the CSS in a `<style>` tag. No external dependencies.

#### HTML Structure

```html
<div class="reading-list">
  <style>
    .reading-list {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 720px;
      margin: 0 auto;
    }
    .reading-list .reading-updated {
      font-size: 0.85em;
      color: #888;
      margin-bottom: 20px;
    }
    .reading-card {
      border: 1px solid #e5e5e5;
      border-radius: 8px;
      padding: 16px 18px;
      margin-bottom: 14px;
    }
    .reading-title {
      font-size: 1em;
      font-weight: 600;
      color: #1a1a1a;
      margin-bottom: 2px;
    }
    .reading-author {
      font-size: 0.85em;
      color: #666;
      margin-bottom: 8px;
    }
    .reading-take {
      font-size: 0.9em;
      color: #444;
      line-height: 1.5;
    }
  </style>

  <div class="reading-updated">Updated {date}</div>

  <div class="reading-card">
    <div class="reading-title">{Title}</div>
    <div class="reading-author">{Author}</div>
    <div class="reading-take">{1-2 sentence take}</div>
  </div>

  <!-- repeat for each book -->

</div>
```

#### Style rules
- One card per book. Cards in purchase_date descending order (same as script output with `--sort recent`).
- No progress percentages. Audible's tracking is unreliable.
- No emojis.
- Authors: if multiple, join with ", ".

### Step 4: Save and display

1. Save HTML to `~/Documents/What Im Reading/what-im-reading.html`
2. Print the full HTML to terminal
3. Print a brief summary: number of books shown, date generated

### Step 5: Squarespace instructions

After generating, remind Jason:
1. Go to the "What I'm Reading" page on jasonhorne.org
2. Replace the existing Code Block content (or add a new Code Block)
3. Paste the HTML
4. Save and publish

## Notes

- Sort order: always purchase_date descending. This is the best proxy for "most recently started" since Audible doesn't expose a reliable start date.
- Do not filter out finished books. If it has any percent_complete > 0, include it. The finished books at the bottom add context.
- If the script fails (auth error, network issue), report the error clearly and stop. Do not generate HTML from stale data.
- The output directory `~/Documents/What Im Reading/` must exist. Create it if it doesn't.
