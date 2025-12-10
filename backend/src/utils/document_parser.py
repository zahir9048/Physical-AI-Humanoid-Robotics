"""
Document parser for MDX/MD files to extract content for the RAG system
"""
import os
from pathlib import Path
from typing import List, Dict, Any
import markdown
from markdown import Extension
from markdown.preprocessors import Preprocessor
import re


class MDXPreprocessor(Preprocessor):
    """
    Preprocessor to handle MDX-specific syntax that might interfere with regular markdown parsing
    """
    def run(self, lines):
        # Remove MDX import/export statements as they're not needed for content extraction
        filtered_lines = []
        for line in lines:
            if not (line.strip().startswith('import') or line.strip().startswith('export')):
                filtered_lines.append(line)
            else:
                # Skip lines that are imports/exports but keep content
                continue
        return filtered_lines


class MDXExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(MDXPreprocessor(), 'mdx_preprocessor', 175)


def parse_mdx_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse an MDX file and extract content, metadata, and structure
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract frontmatter if present (between --- delimiters)
    frontmatter = {}
    content_without_frontmatter = content

    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if frontmatter_match:
        frontmatter_text = frontmatter_match.group(1)
        content_without_frontmatter = frontmatter_match.group(2)

        # Simple frontmatter parsing (could be enhanced with pyyaml if needed)
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip().strip('"\'')

    # Parse markdown content to extract sections and headings
    md = markdown.Markdown(extensions=[MDXExtension(), 'meta', 'tables', 'fenced_code'])
    html_content = md.convert(content_without_frontmatter)

    # Extract text content
    text_content = _extract_text_from_html(html_content)

    # Extract headings and structure
    headings = _extract_headings(content_without_frontmatter)

    return {
        'title': frontmatter.get('title', _extract_title_from_content(content_without_frontmatter)),
        'content': text_content,
        'headings': headings,
        'metadata': frontmatter,
        'file_path': str(file_path),
        'section_structure': _build_section_structure(content_without_frontmatter, headings)
    }


def _extract_text_from_html(html: str) -> str:
    """
    Extract plain text from HTML content
    """
    # Remove HTML tags but preserve content
    clean_text = re.sub(r'<[^>]+>', ' ', html)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text


def _extract_headings(content: str) -> List[Dict[str, Any]]:
    """
    Extract headings from markdown content
    """
    headings = []
    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Match markdown headings (# ## ### etc.)
        heading_match = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            headings.append({
                'level': level,
                'title': title,
                'line_number': i,
                'content_start': _find_content_start(lines, i)
            })

    return headings


def _find_content_start(lines: List[str], heading_line: int) -> int:
    """
    Find where content starts after a heading
    """
    for i in range(heading_line + 1, len(lines)):
        line = lines[i].strip()
        # Skip empty lines and subheadings
        if line and not line.startswith('#'):
            return i
    return heading_line + 1


def _build_section_structure(content: str, headings: List[Dict]) -> List[Dict[str, Any]]:
    """
    Build a structure of sections based on headings
    """
    if not headings:
        return [{'title': 'Content', 'content': content, 'start': 0, 'end': len(content)}]

    sections = []
    lines = content.split('\n')

    for i, heading in enumerate(headings):
        start_line = heading['content_start']
        end_line = len(lines)  # Default to end of content

        # Find the next heading to determine end of current section
        if i + 1 < len(headings):
            end_line = headings[i + 1]['line_number']

        # Extract content between start and end
        section_content_lines = lines[start_line:end_line]
        section_content = '\n'.join(section_content_lines).strip()

        sections.append({
            'title': heading['title'],
            'content': section_content,
            'start_line': start_line,
            'end_line': end_line,
            'level': heading['level']
        })

    return sections


def _extract_title_from_content(content: str) -> str:
    """
    Extract title from content (first heading or first line)
    """
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()  # Remove '# ' prefix
        elif line.startswith('## '):
            return line[3:].strip()  # Remove '## ' prefix
    return content[:50] + "..." if len(content) > 50 else content


def parse_document_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a document file based on its extension
    """
    if file_path.suffix.lower() in ['.md', '.mdx']:
        return parse_mdx_file(file_path)
    elif file_path.suffix.lower() == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return {
            'title': file_path.stem,
            'content': content,
            'headings': [],
            'metadata': {},
            'file_path': str(file_path),
            'section_structure': [{'title': file_path.stem, 'content': content, 'start': 0, 'end': len(content)}]
        }
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")