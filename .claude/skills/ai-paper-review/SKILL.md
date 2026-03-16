---
name: ai-paper-review
description: Review a student's "AI Leading and Learning" paper and insert Word comments with rubric-based feedback. For ETSU Educational Leadership courses.
argument-hint: "[file-path]"
---

Review a student paper and insert Word comments with substantive feedback tied to the assignment rubric.

Target file: $ARGUMENTS

## Supported Assignments

### ai-leading-learning (default)
**AI: Leading and Learning** — 8-10 page APA 7th edition paper with five pillars.

#### Five Pillars to Evaluate

1. **Define & Contextualize**: Does the paper define AI in the K-12 landscape? Does it go beyond "what it is" to explain "why it matters" for school improvement and instructional leadership?

2. **Research & Policy Review**: Are there at least five scholarly or credible sources synthesized (not just summarized)? Does it address AI's impact on learning outcomes, teacher workload, and data privacy?

3. **Instructional Leadership Analysis**: Are AI implementation strategies explicitly connected to TILS Standards A-D? Are specific standard indicators cited, not just general references?

4. **Risks & Ethical Considerations**: Does the paper critically examine algorithmic bias, the digital divide in access, and student data protection under FERPA?

5. **Evidence-Based Recommendations**: Are there 3-5 actionable strategies? Are they aligned with a school mission? Do they promote equitable student success? Are they grounded in the research reviewed earlier in the paper?

#### Criteria for Success (comment on these)

- **APA Formatting**: Correct citations, headings (Level 1 and 2), running head, references page, 12pt Times New Roman or similar, double spacing, 1-inch margins
- **Critical Synthesis**: Is the student comparing and contrasting perspectives, or just summarizing sources one by one?
- **Standard Alignment**: Are connections between AI strategies and specific TILS/PSEL indicators clear and explicit?
- **Actionability**: Are recommendations realistic and grounded in the research reviewed, or generic/aspirational?
- **Page Length**: Is the paper within the 8-10 page requirement (not counting title page and references)?

## Comment Categories

When reviewing, organize feedback into these categories and prefix each comment accordingly:

- **[Strength]** — Something done well; reinforce good practice
- **[Content]** — Missing content, shallow treatment, or factual issues
- **[Synthesis]** — Where the student is summarizing instead of synthesizing; suggest how to compare/contrast
- **[TILS]** — Missing or weak connections to specific TILS Standards A-D; note which standard applies
- **[APA]** — Formatting, citation, or reference errors
- **[Evidence]** — Claims made without supporting citations, or recommendations not grounded in the reviewed research
- **[Ethics]** — Gaps in the risks/ethical analysis (bias, digital divide, FERPA)
- **[Clarity]** — Writing quality issues: awkward phrasing, vague language, unclear arguments
- **[Typo]** — Spelling or grammar errors

## TILS Standards Reference (for evaluating Pillar 3)

Use these when checking standard alignment:

- **Standard A: Instructional Leadership for Continuous Improvement** — Focus on high-quality instruction, data-driven decisions, curriculum alignment, and continuous improvement processes
- **Standard B: Culture for Teaching and Learning** — Establishing a culture of high expectations, equity, and professional growth for all stakeholders
- **Standard C: Professional Learning and Growth** — Leading professional development, fostering collaborative learning communities, and supporting teacher growth
- **Standard D: Resource Management** — Strategic allocation of fiscal, human, and technological resources to support the school's mission

## Agent Teams Strategy

For comprehensive reviews, use agent teams to parallelize pillar evaluation:

### Team Setup

1. **Create the team**: `TeamCreate` with `team_name: "paper-review"`.
2. **Read the document first** to extract all paragraph text and identify section boundaries.
3. **Create 3 tasks** via `TaskCreate`:
   - **Content reviewer**: Evaluate Pillars 1-3 (Define & Contextualize, Research & Policy Review, Instructional Leadership Analysis). Check for synthesis vs. summary and TILS standard connections.
   - **Ethics reviewer**: Evaluate Pillars 4-5 (Risks & Ethical Considerations, Evidence-Based Recommendations). Check recommendations are actionable and research-grounded.
   - **Format reviewer**: Check APA formatting, typos, grammar, page length, and source count (minimum 5 scholarly sources).
4. **Spawn 3 teammates** via `Agent` tool with `team_name: "paper-review"`, names: `content-reviewer`, `ethics-reviewer`, `format-reviewer`. Use `subagent_type: "general-purpose"`. Launch all in a single message.
5. **Pass document content and paragraph indices** to each teammate so they can return precise locations.
6. Each teammate reviews its assigned areas and returns comments: `{para_index, search_text, comment_text, category}`.
7. **Coordinator merges all comments**, inserts into the document using the technique below, and saves.
8. **Shut down teammates** and `TeamDelete`.

## Technical Implementation

Use the same Word comment insertion technique as the `doc-review` skill:

```python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from lxml import etree
from docx.opc.part import Part
from docx.opc.packuri import PackURI
import zipfile, shutil, os, copy

# XML namespace constants
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

# ── build_comments_xml ──────────────────────────────────────────────
def build_comments_xml(comments_data):
    """Build word/comments.xml from a list of dicts:
       [{id, author, date, text}, ...]
    """
    root = etree.Element(f'{{{W}}}comments', nsmap={'w': W, 'w14': W14})
    for c in comments_data:
        comment = etree.SubElement(root, f'{{{W}}}comment')
        comment.set(f'{{{W}}}id', str(c['id']))
        comment.set(f'{{{W}}}author', c['author'])
        comment.set(f'{{{W}}}date', c['date'])
        comment.set(f'{{{W}}}initials', ''.join(w[0] for w in c['author'].split()))
        p = etree.SubElement(comment, f'{{{W}}}p')
        # paragraph style
        ppr = etree.SubElement(p, f'{{{W}}}pPr')
        pstyle = etree.SubElement(ppr, f'{{{W}}}pStyle')
        pstyle.set(f'{{{W}}}val', 'CommentText')
        # annotationRef run (first)
        ar_run = etree.SubElement(p, f'{{{W}}}r')
        ar_rpr = etree.SubElement(ar_run, f'{{{W}}}rPr')
        ar_rstyle = etree.SubElement(ar_rpr, f'{{{W}}}rStyle')
        ar_rstyle.set(f'{{{W}}}val', 'CommentReference')
        etree.SubElement(ar_run, f'{{{W}}}annotationRef')
        # text run
        r = etree.SubElement(p, f'{{{W}}}r')
        t = etree.SubElement(r, f'{{{W}}}t')
        t.text = c['text']
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

# ── build_comments_extended_xml ─────────────────────────────────────
def build_comments_extended_xml(comments_data):
    root = etree.Element(f'{{{W15}}}commentsEx', nsmap={'w15': W15})
    for c in comments_data:
        ce = etree.SubElement(root, f'{{{W15}}}commentEx')
        ce.set(f'{{{W15}}}paraId', f'{c["id"]:08X}')
        ce.set(f'{{{W15}}}done', '0')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

# ── build_comments_ids_xml ──────────────────────────────────────────
def build_comments_ids_xml(comments_data):
    root = etree.Element(f'{{{W16CID}}}commentsIds',
                         nsmap={'w16cid': W16CID}) if False else \
           etree.Element(f'{{{W15}}}commentsIds', nsmap={'w15': W15})
    # Simplified: use w15 namespace for IDs
    for c in comments_data:
        ci = etree.SubElement(root, f'{{{W15}}}commentId')
        ci.set(f'{{{W15}}}paraId', f'{c["id"]:08X}')
        ci.set(f'{{{W15}}}durableId', str(0x60000000 + c['id']))
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

# ── inject_comment_anchors ──────────────────────────────────────────
def inject_comment_anchors(paragraph, search_text, comment_id):
    """Insert commentRangeStart/End + commentReference into a paragraph."""
    found = False
    for run in paragraph.runs:
        if search_text.lower() in (run.text or "").lower():
            comment_start = OxmlElement('w:commentRangeStart')
            comment_start.set(qn('w:id'), str(comment_id))
            run.element.addprevious(comment_start)
            comment_end = OxmlElement('w:commentRangeEnd')
            comment_end.set(qn('w:id'), str(comment_id))
            run.element.addnext(comment_end)
            ref_run = OxmlElement('w:r')
            rpr = etree.SubElement(ref_run, f'{{{W}}}rPr')
            rstyle = etree.SubElement(rpr, f'{{{W}}}rStyle')
            rstyle.set(f'{{{W}}}val', 'CommentReference')
            comment_ref = OxmlElement('w:commentReference')
            comment_ref.set(qn('w:id'), str(comment_id))
            ref_run.append(comment_ref)
            comment_end.addnext(ref_run)
            found = True
            break
    if not found:
        p_element = paragraph._element
        comment_start = OxmlElement('w:commentRangeStart')
        comment_start.set(qn('w:id'), str(comment_id))
        p_element.insert(0, comment_start)
        comment_end = OxmlElement('w:commentRangeEnd')
        comment_end.set(qn('w:id'), str(comment_id))
        p_element.append(comment_end)
        ref_run = OxmlElement('w:r')
        rpr = etree.SubElement(ref_run, f'{{{W}}}rPr')
        rstyle = etree.SubElement(rpr, f'{{{W}}}rStyle')
        rstyle.set(f'{{{W}}}val', 'CommentReference')
        comment_ref = OxmlElement('w:commentReference')
        comment_ref.set(qn('w:id'), str(comment_id))
        ref_run.append(comment_ref)
        p_element.append(ref_run)

# ── ensure_content_types ────────────────────────────────────────────
def ensure_content_types(ct_xml_bytes):
    """Add Override entries for comments parts to [Content_Types].xml."""
    root = etree.fromstring(ct_xml_bytes)
    overrides = {
        '/word/comments.xml':
            'application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml',
        '/word/commentsExtended.xml':
            'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml',
        '/word/commentsIds.xml':
            'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml',
    }
    existing = {el.get('PartName') for el in root.findall(f'{{{CT_NS}}}Override')}
    for part_name, content_type in overrides.items():
        if part_name not in existing:
            ov = etree.SubElement(root, f'{{{CT_NS}}}Override')
            ov.set('PartName', part_name)
            ov.set('ContentType', content_type)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

# ── write_reviewed_docx ─────────────────────────────────────────────
def write_reviewed_docx(doc, src_path, out_path, comments_data):
    """Save the doc with proper comments, commentsExtended, commentsIds,
       and patched [Content_Types].xml so Word renders comments natively."""
    # 1. Save doc to a temp file (gets document.xml + rels right)
    tmp_path = out_path + '.tmp.docx'
    doc.save(tmp_path)

    # 2. Build the three comment XML blobs
    comments_bytes = build_comments_xml(comments_data)
    extended_bytes = build_comments_extended_xml(comments_data)
    ids_bytes      = build_comments_ids_xml(comments_data)

    # 3. Rewrite the zip, injecting comment parts + patched content types
    with zipfile.ZipFile(tmp_path, 'r') as zin, \
         zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == '[Content_Types].xml':
                data = ensure_content_types(data)
            zout.writestr(item, data)
        zout.writestr('word/comments.xml', comments_bytes)
        zout.writestr('word/commentsExtended.xml', extended_bytes)
        zout.writestr('word/commentsIds.xml', ids_bytes)

    os.remove(tmp_path)
```

## Steps

1. **Locate and load the file** — resolve the path, verify it's a valid .docx
2. **Read the full document** — extract all paragraph text to understand structure and content
3. **Identify the paper's sections** — map which paragraphs correspond to each of the five pillars
4. **Evaluate each pillar** against the rubric criteria:
   - Note strengths to reinforce
   - Identify gaps, shallow treatment, or missing elements
   - Check for synthesis vs. summary
   - Verify TILS standard connections are explicit and specific
   - Confirm recommendations are actionable and research-grounded
5. **Check APA formatting** — headings, in-text citations, reference formatting
6. **Check for typos and grammar issues**
7. **Count sources** — verify at least 5 scholarly/credible sources are used
8. **Check page length** — estimate based on paragraph count (roughly 25-30 paragraphs per page of double-spaced text)
9. **Build and insert all comments** at specific locations in the document
10. **Save the file** (overwrite in place unless user requests a copy)
11. **Open in Word** using `open -a "Microsoft Word" "<path>"`
12. **Report summary** — total comment count broken down by category, overall assessment of which pillars are strong and which need work

## Rules

- Author name on all comments: "Jason Horne"
- Date: use today's date in ISO format
- Be constructive and specific — every critique should include direction on how to improve
- Start with strengths before addressing weaknesses
- Do NOT rewrite the student's work in comments — point them toward what to fix and why
- Flag when a student is summarizing a source rather than synthesizing it with other sources
- When a TILS connection is weak, name the specific standard and indicator that applies
- Note if recommendations are generic ("schools should use AI") vs. actionable ("implement a monthly AI tool pilot program with teacher feedback surveys")
- Always check both paragraphs and tables for content
- If the paper has fewer than 5 sources, flag it explicitly
- If the paper is significantly under or over page length, note it
