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

### Cached takes
`~/Documents/What Im Reading/book-takes.json` stores previously written book descriptions keyed by Audible ASIN. Load this file before generating takes and only write new takes for books not already in the cache. Update the cache with any new entries after generating.

### Output
- HTML file: `~/Documents/What Im Reading/what-im-reading.html`
- Also printed to terminal for copy-paste into Squarespace

## Workflow

### Step 1: Pull Audible data

Run:
```
/opt/anaconda3/bin/python3 ~/Scripts/audible_listening.py --sort recent
```

This returns JSON with all books that have any listening progress (percent_complete > 0) OR are marked as finished (is_finished == true), sorted by purchase_date descending. Audible often reports 0% progress for completed books (different devices, full-cast editions), so the script includes both conditions.

### Step 2: Load cached takes

Read `~/Documents/What Im Reading/book-takes.json`. Match books from Step 1 by ASIN. Only write new takes for books that don't already have an entry in the cache.

### Step 3: Generate brief takes (new books only)

For each NEW book (not in cache), write a 1-2 sentence take in Jason's voice:
- Direct and opinionated. Say what it is and whether it's worth the time.
- Specific details over vague praise ("good pacing" is useless; "the author spends too long on X" is useful).
- No hedging. No "I found this interesting." Just the take.
- Keep it punchy. These are captions, not reviews.

If you don't have enough context to write a real take from the title and author alone, write a neutral placeholder like: "Just started this one." or "Still early, but the premise is [X]."

Update the cache file with any new entries.

### Step 4: Categorize books

Split books into two sections:
- **Currently Listening**: books where `is_finished == false` AND `percent_complete > 0`
- **The Shelf**: everything else (finished books, or books with any progress that are marked finished)

### Step 5: Generate HTML

Produce a self-contained HTML block styled for Squarespace. Inline the CSS in a `<style>` tag. No external dependencies.

#### HTML Structure

Use the `#reading-page` scoped design with:
- A centered page header with title and "Updated {date}" timestamp
- "CURRENTLY LISTENING" section: responsive grid with `card-current` class (blue left border accent `#4a6fa5`)
- "THE SHELF" section: 2-column grid on desktop, 1-column on mobile, with `card-shelf` class (light gray left border)
- White card backgrounds with subtle box-shadow
- Georgia serif for titles/body, Arial for metadata labels
- Author names cleaned: remove "- introduction", "- translator", "Dr. Dr." suffixes

#### Exclusions
- Filter out "Your First Listen" (ASIN B002V8N37Q) and "Go the F--k to Sleep" (ASIN B00551W570)

#### Style rules
- Cards sorted by purchase_date descending within each section
- No progress percentages. Audible's tracking is unreliable.
- No emojis.
- Authors: if multiple, join with ", ". Clean suffixes.

### Step 6: Save and display

1. Save HTML to `~/Documents/What Im Reading/what-im-reading.html`
2. Print the full HTML to terminal
3. Print a brief summary: number of books shown (current + shelf), date generated

### Step 7: Squarespace instructions

After generating, remind Jason:
1. Go to the "What I'm Reading" page on jasonhorne.org
2. Replace the existing Code Block content (or add a new Code Block)
3. Paste the HTML
4. Save and publish

## Notes

- Sort order: always purchase_date descending. This is the best proxy for "most recently started" since Audible doesn't expose a reliable start date.
- Include books where `percent_complete > 0` OR `is_finished == true`. Audible reports 0% progress for many completed books.
- If the script fails (auth error, network issue), report the error clearly and stop. Do not generate HTML from stale data.
- The output directory `~/Documents/What Im Reading/` must exist. Create it if it doesn't.
- If Jason says a book is finished, move it from Currently Listening to the top of The Shelf and update the take if it was a placeholder.
