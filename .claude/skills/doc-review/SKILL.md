---
name: doc-review
description: Review a .docx file and insert Word comments for typos, errors, formatting issues, and other feedback. Works for dissertations, proposals, reports, or any Word document.
argument-hint: "[file-path] [optional: specific corrections or 'full review']"
---

Review a Word document and insert comments directly into the .docx file using python-docx and lxml XML manipulation.

Target file: $ARGUMENTS

## Modes

### 1. User-provided corrections
If the user provides a list of specific errors/corrections, insert a Word comment at each location in the document.

### 2. Full review (user says "full review" or similar)
Read the document and identify:
- Spelling errors and typos
- Grammar issues
- Inconsistent author name spellings
- Incomplete or malformed citations/references
- Template placeholder text that hasn't been filled in
- Tense inconsistencies
- Missing content (empty sections, placeholder tables)
- Formatting issues (inconsistent hyphenation, capitalization)

Then insert Word comments at each finding.

## How to insert Word comments

Use this Python approach with `python-docx` and `lxml`:

Use direct zip/XML manipulation. Do NOT rely on python-docx's high-level API for comments because `DocumentPart` does not expose `comments_part` in current versions.

### Required libraries
```python
import zipfile
import shutil
import os
import random
from lxml import etree
from datetime import datetime
```

### XML namespaces
```python
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
W15 = "http://schemas.microsoft.com/office/word/2012/wordml"
W16CID = "http://schemas.microsoft.com/office/word/2016/wordml/cid"
RELS_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

COMMENT_AUTHOR = "Jason Horne"
COMMENT_DATE = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_para_id():
    return format(random.randint(0, 0xFFFFFFFF), '08X').upper()
```

### Build comments.xml

IMPORTANT: Use `nsmap=` in the Element constructor for namespace declarations. Do NOT use `root.set('xmlns:w', ...)` as lxml will raise `ValueError: Invalid attribute name`. Each comment paragraph MUST include a `CommentText` paragraph style and an `annotationRef` run, or Word will render comments as hashtags (#).

```python
def build_comments_xml(comments_list):
    nsmap = {'w': W, 'w14': W14}
    root = etree.Element(f'{{{W}}}comments', nsmap=nsmap)

    for c in comments_list:
        comment_elem = etree.SubElement(root, f'{{{W}}}comment')
        comment_elem.set(f'{{{W}}}id', str(c['id']))
        comment_elem.set(f'{{{W}}}author', c['author'])
        comment_elem.set(f'{{{W}}}date', c['date'])

        inner_p = etree.SubElement(comment_elem, f'{{{W}}}p')
        inner_p.set(f'{{{W14}}}paraId', c['inner_para_id'])
        inner_p.set(f'{{{W14}}}textId', '77777777')

        # Paragraph style: CommentText (required for Word to render)
        ppr = etree.SubElement(inner_p, f'{{{W}}}pPr')
        pstyle = etree.SubElement(ppr, f'{{{W}}}pStyle')
        pstyle.set(f'{{{W}}}val', 'CommentText')

        # First run: annotationRef with CommentReference style (required)
        ref_run = etree.SubElement(inner_p, f'{{{W}}}r')
        ref_rpr = etree.SubElement(ref_run, f'{{{W}}}rPr')
        ref_rstyle = etree.SubElement(ref_rpr, f'{{{W}}}rStyle')
        ref_rstyle.set(f'{{{W}}}val', 'CommentReference')
        etree.SubElement(ref_run, f'{{{W}}}annotationRef')

        # Second run: the actual comment text
        text_run = etree.SubElement(inner_p, f'{{{W}}}r')
        t = etree.SubElement(text_run, f'{{{W}}}t')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = c['text']

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
```

### Build commentsExtended.xml

```python
def build_comments_extended_xml(comments_list):
    nsmap = {'w15': W15}
    root = etree.Element(f'{{{W15}}}commentsEx', nsmap=nsmap)
    for c in comments_list:
        ex = etree.SubElement(root, f'{{{W15}}}commentEx')
        ex.set(f'{{{W15}}}paraId', c['inner_para_id'])
        ex.set(f'{{{W15}}}done', '0')
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
```

### Build commentsIds.xml

```python
def build_comments_ids_xml(comments_list):
    nsmap = {'w16cid': W16CID}
    root = etree.Element(f'{{{W16CID}}}commentsIds', nsmap=nsmap)
    for c in comments_list:
        cid_elem = etree.SubElement(root, f'{{{W16CID}}}commentId')
        cid_elem.set(f'{{{W16CID}}}paraId', c['inner_para_id'])
        cid_elem.set(f'{{{W16CID}}}durableId', c['inner_para_id'])
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
```

### Inject comment anchors into document.xml

```python
def inject_comment_anchors(doc_xml_bytes, para_comment_map):
    """
    para_comment_map: {para_index: comment_id}
    """
    root = etree.fromstring(doc_xml_bytes)
    paragraphs = root.findall(f'.//{{{W}}}p')

    for para_idx, comment_id in para_comment_map.items():
        if para_idx >= len(paragraphs):
            continue
        para = paragraphs[para_idx]

        range_start = etree.Element(f'{{{W}}}commentRangeStart')
        range_start.set(f'{{{W}}}id', str(comment_id))

        range_end = etree.Element(f'{{{W}}}commentRangeEnd')
        range_end.set(f'{{{W}}}id', str(comment_id))

        ref_run = etree.Element(f'{{{W}}}r')
        rpr = etree.SubElement(ref_run, f'{{{W}}}rPr')
        rstyle = etree.SubElement(rpr, f'{{{W}}}rStyle')
        rstyle.set(f'{{{W}}}val', 'CommentReference')
        ref = etree.SubElement(ref_run, f'{{{W}}}commentReference')
        ref.set(f'{{{W}}}id', str(comment_id))

        ppr = para.find(f'{{{W}}}pPr')
        insert_pos = (list(para).index(ppr) + 1) if ppr is not None else 0
        para.insert(insert_pos, range_start)
        para.append(range_end)
        para.append(ref_run)

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
```

### Ensure comment relationships in document.xml.rels

```python
COMMENT_RELS = [
    (
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments',
        'comments.xml'
    ),
    (
        'http://schemas.microsoft.com/office/2011/relationships/commentsExtended',
        'commentsExtended.xml'
    ),
    (
        'http://schemas.microsoft.com/office/2016/09/relationships/commentsIds',
        'commentsIds.xml'
    ),
]

def ensure_comment_rels(rels_xml_bytes):
    root = etree.fromstring(rels_xml_bytes)
    existing_targets = {r.get('Target') for r in root.findall(f'{{{RELS_NS}}}Relationship')}
    existing_ids = {r.get('Id') for r in root.findall(f'{{{RELS_NS}}}Relationship')}

    for rel_type, target in COMMENT_RELS:
        if target not in existing_targets:
            base_id = 'rIdComment' + target.split('.')[0].split('comments')[-1].capitalize()
            rid = base_id
            n = 2
            while rid in existing_ids:
                rid = base_id + str(n)
                n += 1
            rel = etree.SubElement(root, f'{{{RELS_NS}}}Relationship')
            rel.set('Id', rid)
            rel.set('Type', rel_type)
            rel.set('Target', target)
            existing_ids.add(rid)

    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
```

### Ensure content types in [Content_Types].xml

CRITICAL: Without these Override entries, Word cannot parse the comment XML parts and will render comments as hashtags (#).

```python
COMMENT_CONTENT_TYPES = [
    ('/word/comments.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml'),
    ('/word/commentsExtended.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml'),
    ('/word/commentsIds.xml', 'application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml'),
]

def ensure_content_types(ct_xml_bytes):
    root = etree.fromstring(ct_xml_bytes)
    existing_parts = {o.get('PartName') for o in root.findall(f'{{{CT_NS}}}Override')}
    for part_name, content_type in COMMENT_CONTENT_TYPES:
        if part_name not in existing_parts:
            override = etree.SubElement(root, f'{{{CT_NS}}}Override')
            override.set('PartName', part_name)
            override.set('ContentType', content_type)
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
```

### Main write function

```python
def write_reviewed_docx(input_path, output_path, comments_to_add):
    """
    comments_to_add: list of dicts:
        para_index (int): index into all <w:p> elements in document.xml
        text (str): comment text
        category (str): for terminal summary
    """
    shutil.copy2(input_path, output_path)

    comments_list = []
    para_comment_map = {}
    for i, item in enumerate(comments_to_add):
        inner_para_id = generate_para_id()
        comments_list.append({
            'id': i,
            'author': COMMENT_AUTHOR,
            'date': COMMENT_DATE,
            'text': item['text'],
            'inner_para_id': inner_para_id,
        })
        para_comment_map[item['para_index']] = i

    comments_xml = build_comments_xml(comments_list)
    comments_ext_xml = build_comments_extended_xml(comments_list)
    comments_ids_xml = build_comments_ids_xml(comments_list)

    with zipfile.ZipFile(output_path, 'r') as z:
        doc_xml_bytes = z.read('word/document.xml')
        ct_bytes = z.read('[Content_Types].xml')
        all_names = z.namelist()
        rels_name = 'word/_rels/document.xml.rels'
        rels_bytes = z.read(rels_name) if rels_name in all_names else None

    modified_doc = inject_comment_anchors(doc_xml_bytes, para_comment_map)
    modified_rels = ensure_comment_rels(rels_bytes) if rels_bytes else None
    modified_ct = ensure_content_types(ct_bytes)

    tmp = output_path + '.tmp'
    skip = {'word/comments.xml', 'word/commentsExtended.xml', 'word/commentsIds.xml'}

    with zipfile.ZipFile(output_path, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename in skip:
                    continue
                elif item.filename == 'word/document.xml':
                    zout.writestr(item, modified_doc)
                elif item.filename == rels_name and modified_rels:
                    zout.writestr(item, modified_rels)
                elif item.filename == '[Content_Types].xml':
                    zout.writestr(item, modified_ct)
                else:
                    zout.writestr(item, zin.read(item.filename))

            zout.writestr('word/comments.xml', comments_xml)
            zout.writestr('word/commentsExtended.xml', comments_ext_xml)
            zout.writestr('word/commentsIds.xml', comments_ids_xml)

    os.replace(tmp, output_path)
```

### Reading paragraphs for analysis

Use lxml directly for reading to get accurate paragraph indices for comment anchoring:

```python
def get_paragraphs_with_lxml_index(docx_path):
    """
    Returns list of dicts with lxml_index, style, text.
    Counts all <w:p> in document.xml body to get correct lxml index.
    """
    with zipfile.ZipFile(docx_path) as z:
        doc_xml = z.read('word/document.xml')
    root = etree.fromstring(doc_xml)
    all_paras = root.findall(f'.//{{{W}}}p')

    result = []
    for i, p in enumerate(all_paras):
        texts = [t.text for t in p.iter(f'{{{W}}}t') if t.text]
        text = ''.join(texts).strip()

        ppr = p.find(f'{{{W}}}pPr')
        style = ''
        if ppr is not None:
            pstyle = ppr.find(f'{{{W}}}pStyle')
            if pstyle is not None:
                style = pstyle.get(f'{{{W}}}val', '')

        result.append({'lxml_index': i, 'style': style, 'text': text})

    return result
```

## Agent Teams Strategy (Full Review Mode)

For full document reviews on long documents (50+ pages), use agent teams to parallelize the review:

1. **Create the team**: `TeamCreate` with `team_name: "doc-review"`.
2. **Read the document first** to determine its length and identify logical sections.
3. **Create tasks** via `TaskCreate`, splitting the document by review category:
   - **Spelling/grammar reviewer**: Typos, grammar issues, tense inconsistencies
   - **Citations/references reviewer**: Incomplete or malformed citations, author name consistency, reference formatting
   - **Content reviewer**: Template placeholders, missing content, empty sections, formatting inconsistencies
4. **Spawn 3 teammates** via `Agent` tool with `team_name: "doc-review"`, `subagent_type: "general-purpose"`, named `spelling-reviewer`, `citations-reviewer`, `content-reviewer`. Launch all in a single message.
5. Each teammate reviews the full document for its assigned category and returns comments: `{search_text, comment_text, category}`.
6. **Coordinator merges all comments**, inserts into the document, and saves.
7. **Shut down teammates** and `TeamDelete`.

For short documents or user-provided corrections mode, run as a single agent without teams.

## Steps

1. **Locate the file** — resolve the path, check it exists and is a valid .docx
2. **Read the document** — use `get_paragraphs_with_lxml_index()` to get text and lxml indices
3. **Search for each error** — find the paragraph index containing each search term (case-insensitive)
4. **Build the comment list** — each comment has `para_index`, `text`, and `category`
5. **Write the reviewed .docx** using `write_reviewed_docx()`
6. **Open in Word** using `open -a "Microsoft Word" "<path>"`
7. **Report** — tell the user how many comments were added and summarize the categories

## Rules

- Author name on all comments: "Jason Horne"
- Date on comments: use today's date in ISO format
- Always search both paragraphs AND table cells for error text
- If a search term isn't found, report it to the user rather than silently skipping
- Group comments by category in the summary (typos, citations, template artifacts, etc.)
- For dissertation/proposal reviews, flag tense consistency issues (proposal = future tense, dissertation = past tense)
- Do NOT make direct edits to the text — only insert comments so the author can make their own corrections
- Ensure lxml and python-docx are installed before running (`pip3 install lxml python-docx` if needed)
