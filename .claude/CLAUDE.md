# Claude Code Configuration - Jason B. Horne, Ed.D., MBA, SFO

## Identity

- Assistant Director of Schools for Administration, Greeneville City Schools (GCS)
- Oversees: HR, Finance, Maintenance, Technology, Transportation, Custodial, Nutrition, Data, Coordinated School Health
- Adjunct Professor, ETSU (Educational Leadership)
- Location: Greeneville, Tennessee
- Personal site: jasonhorne.org
- Family: Father to Henry (age 11)

## Core Rules

These apply to every interaction:

1. Bias toward action. Execute immediately rather than asking clarifying questions. If ambiguous, make a reasonable choice and note the assumption.
2. Never speculate about reasons for data patterns (e.g., COVID, demographic shifts) unless explicitly asked.
3. Skip files already processed (e.g., don't re-convert existing PDFs, don't re-download existing data).
4. Test scripts with a small subset before running on a full directory.
5. Keep things simple and practical. Prefer direct action over long explanations.
6. Save research reports as .docx to ~/Documents/Research/<topic-folder>/ or user-specified directory. Use parallel Task agents for comprehensive research.

## Output Style

- Formal but conversational tone
- Concise, no fluff
- Clear structure with headings and bullet points
- Practical recommendations over abstract theory
- Act as a thought partner, not just a writing assistant
- Strong opinions are welcome if grounded in reasoning

## File Organization

- When organizing files, use keyword-based categories by default, NOT fiscal year sorting, unless explicitly requested.
- Fiscal year = July through June (for school files when requested).
- Always confirm the target directory and organizational scheme before moving files.
- Verify correct OneDrive root path before operations.
- When working with OneDrive/iCloud/Google Drive, note that cloud-synced folders may have access limitations.

## Research Reports

- Default save location: `~/Documents/Research/<topic-folder>/` (lowercase-hyphen folder names)
- All research reports saved as .docx format.
- `/research` — education-focused, 6-agent deep dive with TN-specific data
- `/general-research` — general topics, lighter-weight single report
- Both skills save to the same `~/Documents/Research/` base directory.
- `~/Documents/Research/scripts/` holds Python generation scripts (kept separate from reports).
- Use parallel research agents (Task tool) for comprehensive reports.
- Include source counts and Tennessee-specific context when relevant to education topics.
- Do not re-do work that a running agent has already been told to handle.

## macOS Compatibility

- This is a macOS environment. Use zsh (not bash) for shell scripts — macOS bash is outdated and lacks features like associative arrays.
- Be cautious with AppleScript automation — dialog boxes and permissions can block execution.
- Port 5000 is often taken by AirPlay on macOS; use alternative ports for local servers.
- This is a work computer — do NOT suggest enabling SSH/Remote Login or other changes that could violate IT policies.

## Daily Automation Scripts

- User has an existing daily_workflow master orchestration script. New automations should be integrated INTO this file rather than created as separate scripts.
- Always check for existing scripts that handle similar logic before creating new ones.
- Use launchd (not cron) for scheduling on macOS.

## Shell and Scripting

- Always use zsh, not bash. macOS bash is v3.2 and lacks modern features.
- Prefer .command files for clickable Mac automation (double-click in Finder).
- Use launchd for scheduled tasks. Verify plist syntax with `plutil -lint` before loading.
- When modifying existing scripts, preserve working functionality. Only append/modify the relevant section.
- Python 3 for data processing.

## Git and GitHub

Before any push/pull, verify all three: (1) repo is initialized, (2) remote is configured, (3) GitHub CLI `gh` is authenticated. Do not attempt git operations without confirming these first.

This is a work computer. Do not enable SSH or Remote Login. Use Tailscale for remote access if needed.

## Browser Automation & MCP

Puppeteer MCP is configured on this Mac. Use it for website interactions including PowerSchool, Squarespace, and other web apps. When the user asks to control a browser or interact with web UIs, use the Puppeteer MCP — do NOT say browser control is impossible.

For sites requiring login (PowerSchool, Squarespace), expect authentication challenges and plan for them upfront. Test login flows step-by-step before full automation.

Implement robust error handling for disconnections and include reconnection logic.

Google Drive files cannot be accessed via API without credentials; ask the user to download/export manually if needed.

## Domain Knowledge

Apply this context automatically when working in these areas:

- TN School Funding: TISA, ADM, BEP, ED codes
- Finance and Audit: Internal school funds, audit findings, fiscal controls, SBITA
- Legislative: TN education legislation tracking and compliance
- Staffing and HR: Salary studies, evaluations, hiring pipelines
- Technology Governance: Responsible AI adoption, data privacy, ed-tech policy
- Capital Planning: CIP, building projects, operational efficiency
- Strategic Frameworks: Theory of Constraints, operational strategy, process improvement
- Include Tennessee-specific context when the topic relates to education policy or K-12
- Treat school district functions like well-run small businesses inside a public education system

## Primary Workflows

### Enrollment Data Pipeline

- Daily PowerSchool SQL reports: enrollment, GTC, withdrawals
- Processing: `enrollment.py` and `enrollment.command`
- Data directory: `OneDrive-GCS/Python/Enrollment Data/`
- Output: Google Sheets for Looker Studio dashboards
- Also handles Tennessee state education data files (assessments, accountability, demographics)

### AI Newsletters

- Monthly AI newsletters for GCS staff via Smore
- Archive: `OneDrive-GCS/AI/Newsletters/`
- Track shared articles in `AI Newsletter Archive.xlsx` to avoid duplicates
- Generate on the 27th of each month

### Document Processing

- Convert DOCX to PDF frequently
- Merge multiple PDFs into single documents
- Organize contracts and MOUs into Legal/

## Common Task Patterns

1. Organize messy folders by type, date, or topic
2. Create .command automation scripts
3. Download and process TN state education data
4. Analyze data: enrollment, paper usage, staffing, budgets
5. Generate reports and summaries
6. Convert and merge documents
7. Consolidate scattered files (contracts, MOUs into Legal/)
8. Draft policy language, contracts, MOUs
9. Legislative tracking and summarization
10. Training design and professional development materials
11. Strategic planning and board communication documents

## Health Tracking

- Use Dexcom for blood sugar monitoring
- Medical files: `OneDrive-EastTennesseeStateUniversity/Personal/Medical/`

## Key Directories

```
~/Documents/                              # General documents
~/Documents/Research/                     # All research reports, organized by topic subfolder
~/Downloads/                              # Regular cleanup via organize_downloads.sh
~/Scripts/                                # Automation scripts

~/OneDrive-GreenevilleCitySchools/        (alias: OneDrive-GCS)
  ├── AI/                                 # Adoption, Agents, Newsletters, Presentations, Training
  ├── Audits/                             # Reports, Meetings, Notes
  ├── Board/                              # Files, Goals, Items, Policies
  ├── Comms/                              # Communications, Branding, BrightArrow, Letterhead
  ├── Data/                               # EIS, Health Scores, Letter Grades, Op Data, Surveys
  ├── Facilities/                         # Building Plans, Capital Projects, CIP, GCTA
  ├── Finance/                            # Budget, Capital Fund, Reports, Invoices, SBITA, TISA
  ├── HR/                                 # Evaluations, Interns, Interviews, New Teacher Training
  ├── Insurance/                          # Claims, Data, Loss Control, Policies
  ├── Leadership/                         # Team, Retreat
  ├── Legal/                              # Contracts, MOUs, Compliance, Investigations
  ├── Legislative/                        # Breakfast, Updates
  ├── Purchasing/                         # Bids, Copy Paper, ScribOrder
  ├── Python/Enrollment Data/             # Daily enrollment reports
  ├── Salary Study/                       # Research and committee files
  └── School Operations/                  # Safety, Discipline, Nutrition, Code of Conduct

~/OneDrive-EastTennesseeStateUniversity/
  └── Personal/                           # Includes Medical/ subdirectory
```

## Data Processing Rules

- When processing date-based files (fiscal years, reports), validate date parsing logic with a sample before processing the full batch.
- When organizing files, verify the correct root path first, especially for OneDrive and iCloud directories.
- For PowerSchool data, use SQL queries and validate output before bulk operations.
