# Jason Horne - Claude Code Configuration

## General Rules
- When the user says to do something, execute it immediately rather than asking clarifying questions. Bias toward action.
- Never speculate about reasons for data patterns (e.g., COVID) unless explicitly asked for explanations.
- For git operations: check if repo is initialized, remote is configured, and auth is set up BEFORE attempting push/pull.

## File Organization Defaults
- When organizing files, use keyword-based categories by default (NOT fiscal year sorting) unless explicitly requested otherwise.
- Always confirm the target directory and organizational scheme before moving files.
- For OneDrive/iCloud/Google Drive operations, verify the correct root path first.

## About Me
- **Name**: Jason B. Horne, Ed.D.
- **Title**: Assistant Director of Schools for Administration, Greeneville City Schools (GCS)
- **Oversees**: HR, Finance, Maintenance, Technology, Transportation, Custodial, Nutrition, Data, Coordinated School Health
- **Location**: Greeneville, Tennessee
- **Education**: Ed.D. in Educational Leadership + MBA (Business Analytics concentration), ETSU
- **Personal site**: jasonhorne.org
- **Family**: Father to Henry (age 11)

## Communication Preferences
- Formal but conversational tone
- Clear structure with headings and bullet points
- Concise — no fluff
- Practical recommendations over abstract theory
- Act as a thought partner, not just a writing assistant
- Iterative refinement, structured outputs, and actionable deliverables
- Strong opinions are fine if grounded in reasoning

## Professional Domain Knowledge
When working on tasks in these areas, apply relevant context automatically:
- **TN School Funding**: TISA, ADM, BEP, ED codes
- **Finance & Audit**: Internal school funds, audit findings, fiscal controls, SBITA
- **Legislative**: TN education legislation tracking and compliance
- **Staffing & HR**: Salary studies, evaluations, hiring pipelines
- **Technology Governance**: Responsible AI adoption, data privacy, ed-tech policy
- **Capital Planning**: CIP, building projects, operational efficiency
- **Strategic Frameworks**: Theory of Constraints, operational strategy, process improvement
- Thinks operationally — treats school district functions like well-run small businesses inside a public education system

## Primary Work Areas

### 1. Education Data & Enrollment
- Daily PowerSchool SQL reports: enrollment, GTC, withdrawals
- Data goes to: `/Users/hornej/Library/CloudStorage/OneDrive-GreenevilleCitySchools/Python/Enrollment Data/`
- Uses `enrollment.py` and `enrollment.command` for processing
- Uploads to Google Sheets for Looker Studio dashboards
- Tennessee state education data files (assessments, accountability, demographics)

### 2. File Organization
- Prefer organizing files into logical subfolders by date, fiscal year, or topic
- OneDrive locations:
  - GCS: `/Users/hornej/Library/CloudStorage/OneDrive-GreenevilleCitySchools/`
  - ETSU: `/Users/hornej/Library/CloudStorage/OneDrive-EastTennesseeStateUniversity/`
- Downloads folder cleanup script: `/Users/hornej/Scripts/organize_downloads.sh`

### 3. AI Newsletters
- Monthly AI newsletters for GCS staff via Smore
- Archive: `OneDrive-GreenevilleCitySchools/AI/Newsletters/`
- Track shared articles in `AI Newsletter Archive.xlsx` to avoid duplicates
- Generate on the 27th of each month

### 4. Automation Preferences
- Love `.command` files for clickable Mac automation
- Prefer scripts that can be double-clicked in Finder
- Use launchd for scheduled tasks when needed
- Python 3 for data processing

### 5. Document Processing
- Convert DOCX to PDF frequently
- Merge multiple PDFs into single documents
- Organize contracts and MOUs

## Key Directories
```
~/Documents/                    # General documents
~/Downloads/                    # Needs regular cleanup
~/Scripts/                      # Automation scripts
~/OneDrive-GreenevilleCitySchools/
  ├── AI/                      # AI Adoption, Agents, Newsletters, Presentations, Training
  ├── Audits/                  # Reports, Meetings, Notes
  ├── Board/                   # Files, Goals, Items, Policies
  ├── Comms/                   # General, Communications, Branding, BrightArrow, Letterhead
  ├── Data/                    # General, EIS, Health Scores, Letter Grades, Op Data, Population Maps, Surveys
  ├── Facilities/              # General, Building Plans, Capital Projects, CIP, GCTA Property/Purchase
  ├── Finance/                 # Budget, Capital Fund Balance, Financial Reports, Invoices, Receipts, SBITA, TISA
  ├── HR/                      # General, Evaluations, Interns, Interviews, New Teacher Training, Opening Inservice
  ├── Insurance/               # Accident Reports, Claims, Data, Documents, Loss Control, Meetings, Policies
  ├── Leadership/              # Team, Retreat
  ├── Legal/                   # Contracts, MOUs, Compliance, ICE Guidance, Investigations
  ├── Legislative/             # Breakfast, Updates
  ├── Purchasing/              # General, Bids, Copy Paper Usage, Paper, Pepsi, ScribOrder
  ├── Python/Enrollment Data/  # Daily enrollment reports
  ├── Salary Study/            # Salary research and committee files
  └── School Operations/       # Safety, Closures, Discipline Forms, Code of Conduct, Nutrition, Threat Reporting
~/OneDrive-EastTennesseeStateUniversity/Personal/
```

## Preferences
- Fiscal year organization for school files (July-June)
- Skip files already processed (e.g., don't re-convert existing PDFs)
- Test scripts after creating them
- Keep things simple and practical
- Prefer direct action over long explanations

## Common Tasks I Ask For
1. Organize messy folders by type, date, or fiscal year
2. Create automation scripts (.command files)
3. Download and process TN state education data
4. Analyze data (enrollment, paper usage, staffing, etc.)
5. Generate reports and summaries
6. Convert/merge documents
7. Find and consolidate scattered files (contracts in Legal/, MOUs in Legal/)
8. System maintenance and cleanup
9. Draft policy language, contracts, and MOUs
10. Legislative tracking and summarization
11. Training design and professional development materials
12. Strategic planning and board communication documents
13. Research with structured, actionable deliverables

## Health Tracking
- Use Dexcom for blood sugar monitoring
- Medical files: `OneDrive-EastTennesseeStateUniversity/Personal/Medical/`

## Shell Scripting
- Always use zsh (not bash) for macOS scripts. macOS bash is v3.2 and lacks modern features like associative arrays.
- When creating automation scripts, integrate into existing workflow files rather than creating separate standalone scripts.
- Test scripts with a small subset of files before running on the full directory.
- When creating launchd agents, verify plist syntax with `plutil -lint` before loading.
- When modifying automation scripts, preserve existing working functionality and only append/modify the relevant section.

## Browser & External Services
- This Mac has Puppeteer MCP configured for browser automation. Use it when asked to interact with websites.
- Do NOT tell the user browser control is impossible — use MCP/Puppeteer.
- For PowerSchool, Squarespace, and other web apps: use Puppeteer for automation tasks.
- When working with browser automation, implement robust error handling for disconnections and include reconnection logic. Test login flows step-by-step before full automation.
- Google Drive files cannot be accessed via API without credentials; ask user to download/export files manually if needed.

## Research Reports
- Save research reports as .docx format by default to ~/Documents/ or the user-specified directory.
- Use parallel Task agents for comprehensive research.
- Include Tennessee-specific context when the topic relates to education policy or K-12.

## Git & GitHub
- Before attempting to push, verify: git repo is initialized, remote is configured, and GitHub CLI (gh) is authenticated.
- This is a work computer — avoid enabling SSH/Remote Login. Use Tailscale for remote access if needed.

## Data Processing
When processing date-based files (fiscal years, reports), validate date parsing logic with a sample before processing the full batch.
