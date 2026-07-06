#!/usr/bin/env python3
"""
Daytona Skill Generator
=======================
Reads Daytona MDX docs and generates clean markdown skill reference files.
Output goes to skills/daytona/references/.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Daytona skill references from docs and OpenAPI specs."
    )
    parser.add_argument(
        "docs_root",
        type=Path,
        help="Path to Daytona docs content (src/content/docs/en)",
    )
    parser.add_argument(
        "--main-api-spec",
        type=Path,
        required=True,
        help="Path to the main Daytona API OpenAPI spec (JSON or YAML)",
    )
    parser.add_argument(
        "--toolbox-api-spec",
        type=Path,
        required=True,
        help="Path to the Toolbox API OpenAPI spec (JSON or YAML)",
    )
    return parser.parse_args()


args = parse_args()
DOCS_ROOT = args.docs_root.resolve()
if not DOCS_ROOT.is_dir():
    print(f"Error: docs directory not found: {DOCS_ROOT}")
    sys.exit(1)

OUTPUT_ROOT = REPO_ROOT / "skills" / "daytona" / "references"

SDK_LANGUAGES = {
    "python-sdk": "Python",
    "typescript-sdk": "TypeScript",
    "go-sdk": "Go",
    "ruby-sdk": "Ruby",
}

# Core feature docs that get split per-SDK (have syncKey="language" with SDK tabs)
CORE_FEATURE_DOCS = [
    "sandboxes",
    "process-code-execution",
    "file-system-operations",
    "git-operations",
    "snapshots",
    "volumes",
    "ssh-access",
    "vnc-access",
    "computer-use",
    "configuration",
    "declarative-builder",
    "log-streaming",
    "network-limits",
    "language-server-protocol",
    "preview",
    "pty",
    "regions",
    "vpn-connections",
    "getting-started",
]

# Language-agnostic platform docs (no SDK-specific tabs, or only API/CLI tabs)
PLATFORM_DOCS = [
    "limits",
    "organizations",
    "billing",
    "audit-logs",
    "linked-accounts",
    "web-terminal",
    "webhooks",
    "mcp",
    "runners",
    "oss-deployment",
]

# OpenAPI spec paths
MAIN_API_SPEC = args.main_api_spec.resolve()
TOOLBOX_API_SPEC = args.toolbox_api_spec.resolve()
API_OUTPUT = OUTPUT_ROOT / "api"
PLATFORM_OUTPUT = OUTPUT_ROOT / "platform"

# Tags to skip from the main API spec
MAIN_API_SKIP_TAGS = {"admin"}

# Files that get renamed on output to avoid collisions
OUTPUT_NAME_OVERRIDES = {
    "computer-use": "computer-use-guide",
}

# SDK reference files to skip (not useful for the skill)
SDK_SKIP_FILES = {"charts"}


# ---------------------------------------------------------------------------
# MDX Transformation Functions
# ---------------------------------------------------------------------------

def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter (--- ... ---)."""
    m = re.match(r"^---\n.*?\n---\n?", content, re.DOTALL)
    if m:
        return content[m.end():]
    return content


def strip_imports(content: str) -> str:
    """Remove Astro/MDX import lines (not code block imports).

    Only strips import lines that appear OUTSIDE of code blocks (``` fences).
    """
    lines = content.split("\n")
    result = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        if not in_code_block and re.match(r"^import\s+", line):
            continue
        result.append(line)
    return "\n".join(result)


def strip_components(content: str) -> str:
    """Remove visual-only components and artifacts."""
    # <SandboxDiagram /> or <SandboxDiagram/>
    content = re.sub(r"<SandboxDiagram\s*/>", "", content)
    # <ExploreMore /> or <ExploreMore/>
    content = re.sub(r"<ExploreMore\s*/>", "", content)
    # <GuidesList ... />
    content = re.sub(r"<GuidesList[^/]*/>\s*", "", content)
    # {/* JSX comments */}
    content = re.sub(r"\{/\*.*?\*/\}", "", content)
    # HTML entities
    content = content.replace("&mdash;", "—")
    content = content.replace("&nbsp;", " ")
    content = content.replace("&amp;", "&")
    content = content.replace("&lt;", "<")
    content = content.replace("&gt;", ">")
    return content


def convert_label_component(content: str) -> str:
    """Convert <Label>text</Label> to **text**."""
    return re.sub(r"<Label>(.*?)</Label>", r"**\1**", content)


def convert_aside_component(content: str) -> str:
    """Convert <Aside type="X">content</Aside> to blockquote."""
    def _replace_aside(m):
        aside_type = m.group(1) or "note"
        inner = m.group(2).strip()
        label = aside_type.capitalize()
        lines = inner.split("\n")
        result = [f"> **{label}:** {lines[0]}"]
        for line in lines[1:]:
            result.append(f"> {line}" if line.strip() else ">")
        return "\n".join(result)

    content = re.sub(
        r'<Aside\s+type="(\w+)">\s*\n?(.*?)\n?\s*</Aside>',
        _replace_aside,
        content,
        flags=re.DOTALL,
    )
    # Aside without type attribute
    content = re.sub(
        r'<Aside>\s*\n?(.*?)\n?\s*</Aside>',
        lambda m: _replace_aside(type("", (), {"group": lambda self, n: {1: "note", 2: m.group(1)}[n]})()),
        content,
        flags=re.DOTALL,
    )
    return content


def convert_callouts(content: str) -> str:
    """Convert :::note / :::tip / :::caution / :::warning / :::danger callouts."""
    def _replace_callout(m):
        callout_type = m.group(1)
        title = m.group(2)
        body = m.group(3)
        label = callout_type.capitalize()
        if title:
            header = f"> **{label}: {title}**"
        else:
            header = f"> **{label}:**"
        lines = body.strip().split("\n")
        result = [header]
        for line in lines:
            if line.strip():
                result.append(f"> {line}")
            else:
                result.append(">")
        return "\n".join(result) + "\n"

    # :::type[Title] or :::type — allow leading whitespace on both opening and closing :::
    content = re.sub(
        r"^\s*:::(note|tip|caution|warning|danger)(?:\[([^\]]*)\])?\s*\n(.*?)^\s*:::\s*$",
        _replace_callout,
        content,
        flags=re.MULTILINE | re.DOTALL,
    )
    return content


def parse_tabs_blocks(content: str):
    """
    Find all <Tabs...>...</Tabs> blocks and return them as a list of
    (start, end, sync_key, items) where items is a list of (label, inner_content).
    """
    blocks = []
    # Find <Tabs...> opening tags
    pattern = re.compile(r"<Tabs(\s[^>]*)?>", re.DOTALL)
    pos = 0
    while True:
        m = pattern.search(content, pos)
        if not m:
            break
        start = m.start()
        attrs = m.group(1) or ""
        sync_key_match = re.search(r'syncKey="([^"]*)"', attrs)
        sync_key = sync_key_match.group(1) if sync_key_match else None

        # Find matching </Tabs>
        depth = 1
        search_pos = m.end()
        while depth > 0 and search_pos < len(content):
            next_open = content.find("<Tabs", search_pos)
            next_close = content.find("</Tabs>", search_pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                search_pos = next_open + 5
            else:
                depth -= 1
                if depth == 0:
                    end = next_close + len("</Tabs>")
                    break
                search_pos = next_close + 7
        else:
            pos = m.end()
            continue

        # Parse TabItems within this block
        tabs_inner = content[m.end():next_close]
        items = parse_tab_items(tabs_inner)
        blocks.append((start, end, sync_key, items))
        pos = end

    return blocks


def dedent_content(text: str) -> str:
    """Remove common leading whitespace from all lines (like textwrap.dedent but simpler)."""
    lines = text.split("\n")
    # Find minimum indentation of non-empty lines
    min_indent = float("inf")
    for line in lines:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            min_indent = min(min_indent, indent)
    if min_indent == float("inf") or min_indent == 0:
        return text
    return "\n".join(
        line[min_indent:] if len(line) >= min_indent else line
        for line in lines
    )


def parse_tab_items(tabs_inner: str):
    """Parse <TabItem label="X">content</TabItem> from inner content."""
    items = []
    pattern = re.compile(r'<TabItem\s+([^>]*)>', re.DOTALL)
    pos = 0
    while True:
        m = pattern.search(tabs_inner, pos)
        if not m:
            break
        attrs = m.group(1)
        label_match = re.search(r'label="([^"]*)"', attrs)
        label = label_match.group(1) if label_match else ""

        # Find matching </TabItem>
        depth = 1
        search_pos = m.end()
        while depth > 0 and search_pos < len(tabs_inner):
            next_open = tabs_inner.find("<TabItem", search_pos)
            next_close = tabs_inner.find("</TabItem>", search_pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                search_pos = next_open + 8
            else:
                depth -= 1
                if depth == 0:
                    inner = tabs_inner[m.end():next_close]
                    items.append((label, dedent_content(inner).strip()))
                    search_pos = next_close + len("</TabItem>")
                    break
                search_pos = next_close + 10
        pos = search_pos

    return items


def extract_language_tab(content: str, language_label: str) -> str:
    """
    For all <Tabs syncKey="language"> blocks, keep only the tab matching
    language_label. Strip the Tabs/TabItem wrappers.
    Non-language tabs are converted to markdown sections.
    """
    blocks = parse_tabs_blocks(content)
    if not blocks:
        return content

    sdk_labels = set(SDK_LANGUAGES.values())

    # Process in reverse order so indices remain valid
    for start, end, sync_key, items in reversed(blocks):
        # SDK language tabs: keep only the matching language
        if sync_key == "language" and {label for label, _ in items} & sdk_labels:
            replacement = ""
            for label, inner in items:
                if label == language_label:
                    replacement = inner
                    break
        else:
            # Everything else (non-SDK tabs, non-language tabs): convert to markdown
            replacement = convert_non_language_tabs(items)
        content = content[:start] + replacement + content[end:]

    return content


def keep_all_tabs_as_markdown(content: str) -> str:
    """
    For platform docs with no language splitting: convert all tabs to
    markdown sections.
    """
    blocks = parse_tabs_blocks(content)
    if not blocks:
        return content

    for start, end, sync_key, items in reversed(blocks):
        replacement = convert_non_language_tabs(items)
        content = content[:start] + replacement + content[end:]

    return content


def convert_non_language_tabs(items):
    """Convert tab items to markdown bold-labeled sections."""
    parts = []
    for label, inner in items:
        parts.append(f"**{label}:**\n\n{inner}")
    return "\n\n".join(parts)


def resolve_links(content: str, current_sdk: str = None, current_depth: str = "sdk") -> str:
    """
    Resolve internal doc links to skill-relative paths.

    current_sdk: e.g. "python-sdk" when generating per-SDK files
    current_depth: "sdk" for files in sdk folders, "top" for files in references/
    """

    def _resolve(m):
        full = m.group(0)
        prefix = m.group(1)  # [text](
        path = m.group(2)     # the URL
        suffix = m.group(3)   # ) or #anchor...)

        # Keep external URLs
        if path.startswith("http://") or path.startswith("https://") or path.startswith("mailto:"):
            return full

        # Normalize: strip /docs/en/ or /docs/ prefix
        normalized = path
        normalized = re.sub(r"^/docs/en/", "/", normalized)
        normalized = re.sub(r"^/docs/", "/", normalized)

        # Split path and anchor
        anchor = ""
        if "#" in normalized:
            normalized, anchor = normalized.split("#", 1)
            anchor = "#" + anchor

        # Remove trailing slash
        normalized = normalized.rstrip("/")

        # Now resolve based on the normalized path
        resolved = _resolve_path(normalized, anchor, current_sdk, current_depth)
        if resolved is not None:
            return f"{prefix}{resolved}{suffix}"

        # Fallback: return original
        return full

    # Match markdown links: [text](url) or [text](url#anchor)
    content = re.sub(
        r'(\[[^\]]*\]\()([^)]+?)(\))',
        _resolve,
        content,
    )
    return content


def _resolve_path(normalized: str, anchor: str, current_sdk: str, current_depth: str) -> str:
    """Resolve a normalized path to a relative skill path."""

    if not normalized or normalized == "/":
        return None

    # SDK index pages: /python-sdk, /typescript-sdk, etc.
    for sdk in SDK_LANGUAGES:
        if normalized == f"/{sdk}":
            if current_depth == "sdk" and current_sdk:
                if current_sdk == sdk:
                    return f"./README.md{anchor}"
                else:
                    return f"../{sdk}/README.md{anchor}"
            else:
                return f"./{sdk}/README.md{anchor}"

    # Python SDK sync: /python-sdk/sync/X
    m = re.match(r"^/python-sdk/sync/(.+)$", normalized)
    if m:
        name = m.group(1)
        target = f"python-sdk/sync/{name}.md"
        return _relative(target, current_sdk, current_depth) + anchor

    # Python SDK async: /python-sdk/async/async-X or /python-sdk/async/X
    m = re.match(r"^/python-sdk/async/(?:async-)?(.+)$", normalized)
    if m:
        name = m.group(1)
        target = f"python-sdk/async/{name}.md"
        return _relative(target, current_sdk, current_depth) + anchor

    # Python SDK common: /python-sdk/common/X
    m = re.match(r"^/python-sdk/common/(.+)$", normalized)
    if m:
        name = m.group(1)
        target = f"python-sdk/{name}.md"
        return _relative(target, current_sdk, current_depth) + anchor

    # Other SDK pages: /typescript-sdk/X, /go-sdk/X, /ruby-sdk/X
    for sdk in ["typescript-sdk", "go-sdk", "ruby-sdk"]:
        m = re.match(rf"^/{sdk}/(.+)$", normalized)
        if m:
            name = m.group(1)
            target = f"{sdk}/{name}.md"
            return _relative(target, current_sdk, current_depth) + anchor

    # Tools
    if normalized == "/tools/cli":
        if current_depth == "sdk-sub":
            return f"../../cli.md{anchor}"
        elif current_depth == "sdk":
            return f"../cli.md{anchor}"
        elif current_depth == "platform":
            return f"../cli.md{anchor}"
        else:
            return f"./cli.md{anchor}"

    if normalized == "/tools/api" or normalized.startswith("/tools/api"):
        if current_depth == "sdk-sub":
            return f"../../api/README.md{anchor}"
        elif current_depth == "sdk":
            return f"../api/README.md{anchor}"
        elif current_depth == "platform":
            return f"../api/README.md{anchor}"
        else:
            return f"./api/README.md{anchor}"

    # API keys -> SKILL.md#authentication
    if normalized == "/api-keys":
        if current_depth == "sdk-sub":
            return f"../../../SKILL.md#authentication{anchor}"
        elif current_depth == "sdk":
            return f"../../SKILL.md#authentication{anchor}"
        elif current_depth == "platform":
            return f"../../SKILL.md#authentication{anchor}"
        else:
            return f"../SKILL.md#authentication{anchor}"

    # Getting started -> SKILL.md or per-SDK
    # (getting-started is a core feature doc, so it exists in SDK folders)

    # Platform docs (in platform/ subfolder)
    platform_names = [d for d in PLATFORM_DOCS]
    for name in platform_names:
        if normalized == f"/{name}":
            if current_depth == "sdk-sub":
                return f"../../platform/{name}.md{anchor}"
            elif current_depth == "sdk":
                return f"../platform/{name}.md{anchor}"
            elif current_depth == "platform":
                return f"./{name}.md{anchor}"
            else:
                return f"./platform/{name}.md{anchor}"

    # Core feature docs -> per-SDK files
    for name in CORE_FEATURE_DOCS:
        if normalized == f"/{name}":
            output_name = OUTPUT_NAME_OVERRIDES.get(name, name)
            if current_depth in ("sdk", "sdk-sub") and current_sdk:
                if current_depth == "sdk-sub":
                    return f"../{output_name}.md{anchor}"
                return f"./{output_name}.md{anchor}"
            elif current_depth == "top":
                return f"./python-sdk/{output_name}.md{anchor}"
            elif current_depth == "platform":
                return f"../python-sdk/{output_name}.md{anchor}"
            return None

    # Docs we don't convert -> link to external Daytona docs site
    DAYTONA_DOCS_BASE = "https://www.daytona.io/docs/en"
    return f"{DAYTONA_DOCS_BASE}{normalized}{anchor}"


def _relative(target: str, current_sdk: str, current_depth: str) -> str:
    """
    Make a target path relative to the current file's location.
    target: e.g. "python-sdk/sync/sandbox.md"
    current_depth: "sdk" for files in sdk folders, "sdk-sub" for files in sdk subfolders (sync/, async/), "top" for references/
    """
    if current_depth == "sdk-sub" and current_sdk:
        # We're in references/<current_sdk>/sync/ or references/<current_sdk>/async/
        target_parts = target.split("/", 1)
        if target_parts[0] == current_sdk:
            # Same SDK folder — need to go up one level from sync/async
            rest = target_parts[1] if len(target_parts) > 1 else "README.md"
            return f"../{rest}"
        else:
            return f"../../{target}"
    elif current_depth == "sdk" and current_sdk:
        # We're in references/<current_sdk>/
        target_parts = target.split("/", 1)
        if target_parts[0] == current_sdk:
            # Same SDK folder
            return f"./{target_parts[1]}" if len(target_parts) > 1 else f"./README.md"
        else:
            return f"../{target}"
    elif current_depth == "platform":
        # We're in references/platform/
        return f"../{target}"
    else:
        # We're in references/
        return f"./{target}"



def append_see_also_sdk_ref(content: str, sdk: str, module_name: str, depth: str = "sdk") -> str:
    """Append See Also section for SDK API reference files."""
    links = []

    up = "../../" if depth == "sdk-sub" else "../"

    # Link to same module in other SDKs — only if the file exists
    for other_sdk in SDK_LANGUAGES:
        if other_sdk == sdk:
            continue
        sdk_label = SDK_LANGUAGES[other_sdk]
        if other_sdk == "python-sdk":
            target = f"python-sdk/sync/{module_name}.md"
            if not (OUTPUT_ROOT / "python-sdk" / "sync" / f"{module_name}.md").exists():
                continue
        else:
            target = f"{other_sdk}/{module_name}.md"
            if not (OUTPUT_ROOT / other_sdk / f"{module_name}.md").exists():
                continue
        links.append(f"- [{sdk_label} SDK - {module_name}]({up}{target})")

    if not links:
        return content
    return content.rstrip() + "\n\n## See Also\n" + "\n".join(links) + "\n"


def strip_cross_sdk_references(content: str, sdk_label: str = None) -> tuple:
    """
    Strip 'For more information, see the [X SDK]...' blocks from per-SDK feature docs.
    These blocks list links to every SDK's API reference for each method — redundant
    once the doc has been split per-SDK.

    Returns (cleaned_content, sorted_list_of_current_sdk_api_ref_links).
    """
    api_ref_links = set()

    if sdk_label:
        sdk_link_re = re.compile(rf'\[{re.escape(sdk_label)} SDK\]\(([^)]+)\)')
        for m in re.finditer(r'For more information, see the [^\n]*references:', content):
            link_match = sdk_link_re.search(m.group(0))
            if link_match:
                api_ref_links.add(link_match.group(1))

    # Strip: "For more information..." line + blank line + blockquote lines + trailing blank
    content = re.sub(
        r'For more information, see the [^\n]*references:\n\n(?:>[^\n]*\n)*\n?',
        '',
        content,
    )

    return content, sorted(api_ref_links)


def append_see_also_feature(content: str, sdk: str, feature_name: str,
                            api_ref_links: list = None) -> str:
    """Append See Also section for per-SDK feature docs."""
    output_name = OUTPUT_NAME_OVERRIDES.get(feature_name, feature_name)
    links = []

    # Current SDK's API reference file(s) for this topic
    if api_ref_links:
        sdk_label = SDK_LANGUAGES[sdk]
        for link in api_ref_links:
            # Extract name from path: ./sync/computer-use.md -> computer-use
            name = link.rstrip("/").rsplit("/", 1)[-1].replace(".md", "")
            links.append(f"- [{sdk_label} SDK - {name}]({link})")

    # Same feature in other SDKs — only if the file exists
    for other_sdk in SDK_LANGUAGES:
        if other_sdk == sdk:
            continue
        sdk_label = SDK_LANGUAGES[other_sdk]
        target_file = OUTPUT_ROOT / other_sdk / f"{output_name}.md"
        if not target_file.exists():
            continue
        links.append(f"- [{sdk_label} SDK - {output_name}](../{other_sdk}/{output_name}.md)")

    if not links:
        return content
    return content.rstrip() + "\n\n## See Also\n" + "\n".join(links) + "\n"


def append_see_also_platform(content: str, doc_name: str) -> str:
    """Append See Also for platform docs."""
    lines = ["\n\n## See Also\n"]
    for sdk in SDK_LANGUAGES:
        sdk_label = SDK_LANGUAGES[sdk]
        lines.append(f"- [{sdk_label} SDK](../{sdk}/README.md)")
    return content.rstrip() + "\n".join(lines) + "\n"


def generate_toc(content: str, min_lines: int = 100) -> str:
    """
    Prepend a table of contents to files longer than min_lines.

    Extracts ## headings, builds a flat TOC, and inserts it after the
    first # heading (or at the top if none).  Skips files that are short
    or have fewer than 3 sections.
    """
    if content.count("\n") < min_lines:
        return content

    lines = content.split("\n")
    headings = []
    in_code_block = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
        if in_code_block:
            continue
        # Only ## level headings for a scannable TOC
        if stripped.startswith("## ") and not stripped.startswith("### "):
            headings.append(stripped)

    if len(headings) < 3:
        return content

    toc_lines = ["## Contents", ""]
    for h in headings:
        text = h[3:]
        # Strip trailing anchor syntax {#...}
        text = re.sub(r"\s*\{#[^}]*\}", "", text)
        display = text.strip()
        toc_lines.append(f"- {display}")

    toc_lines.append("")
    toc_block = "\n".join(toc_lines)

    # Insert after the first # heading line (not ## or ###)
    insert_pos = None
    in_code = False
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        if stripped.startswith("# ") and not stripped.startswith("## "):
            insert_pos = i + 1
            break

    if insert_pos is not None:
        # Skip blank lines immediately after the title
        while insert_pos < len(lines) and not lines[insert_pos].strip():
            insert_pos += 1
        lines.insert(insert_pos, "\n" + toc_block)
    else:
        lines.insert(0, toc_block + "\n")

    return "\n".join(lines)


def clean_content(content: str) -> str:
    """Clean up common artifacts after transformations."""
    # Remove excessive blank lines (more than 2 consecutive)
    content = re.sub(r"\n{4,}", "\n\n\n", content)
    # Remove trailing whitespace on lines
    content = re.sub(r"[ \t]+$", "", content, flags=re.MULTILINE)
    # Ensure file ends with single newline
    content = content.rstrip() + "\n"
    return content


# ---------------------------------------------------------------------------
# File Processing
# ---------------------------------------------------------------------------

def read_mdx(path: Path) -> str:
    """Read an MDX file, return empty string if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def iter_sdk_mdx(directory: Path, strip_prefix: str = None):
    """
    Yield (name, content) for each .mdx file in directory,
    skipping index.mdx and files in SDK_SKIP_FILES.
    If strip_prefix is set, remove it from the stem (e.g. "async-" -> "").
    """
    if not directory.exists():
        return
    for f in sorted(directory.glob("*.mdx")):
        if f.name == "index.mdx":
            continue
        name = f.stem
        if strip_prefix and name.startswith(strip_prefix):
            name = name[len(strip_prefix):]
        if name in SDK_SKIP_FILES:
            continue
        content = read_mdx(f)
        if content:
            yield name, content


def write_md(path: Path, content: str):
    """Write markdown file, creating directories as needed."""
    content = generate_toc(content)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  -> {path.relative_to(REPO_ROOT)}")


def process_content_common(content: str) -> str:
    """Apply transformations common to all files."""
    content = strip_frontmatter(content)
    content = strip_imports(content)
    content = strip_components(content)
    content = convert_label_component(content)
    content = convert_aside_component(content)
    content = convert_callouts(content)
    return content


# ---------------------------------------------------------------------------
# SDK API Reference Generation
# ---------------------------------------------------------------------------

def process_sdk_file(content: str, sdk: str, name: str, depth: str = "sdk") -> str:
    """Standard pipeline for a single SDK reference file."""
    content = process_content_common(content)
    content = keep_all_tabs_as_markdown(content)
    content = resolve_links(content, sdk, depth)
    content = append_see_also_sdk_ref(content, sdk, name, depth=depth)
    return clean_content(content)


def generate_sdk(sdk: str):
    """Generate reference files for any SDK (Python with sync/async/common, or flat)."""
    print(f"\n=== {SDK_LANGUAGES[sdk]} SDK ===")
    src = DOCS_ROOT / sdk
    dst = OUTPUT_ROOT / sdk

    if not src.exists():
        print(f"  WARNING: Source directory {src} not found, skipping")
        return

    # index.mdx -> README.md
    content = read_mdx(src / "index.mdx")
    if content:
        content = process_content_common(content)
        content = keep_all_tabs_as_markdown(content)
        content = resolve_links(content, sdk, "sdk")
        content = clean_content(content)
        write_md(dst / "README.md", content)

    # Python SDK has sync/async/common subdirs
    if sdk == "python-sdk":
        # sync/*.mdx -> sync/*.md
        for name, content in iter_sdk_mdx(src / "sync"):
            content = process_sdk_file(content, sdk, name, depth="sdk-sub")
            # Prepend cross-link to async counterpart
            if (src / "async" / f"async-{name}.mdx").exists():
                content = f"> For the async version, see [async/{name}.md](../async/{name}.md)\n\n" + content
            write_md(dst / "sync" / f"{name}.md", content)

        # async/async-*.mdx -> async/*.md
        for name, content in iter_sdk_mdx(src / "async", strip_prefix="async-"):
            content = process_sdk_file(content, sdk, name, depth="sdk-sub")
            # Prepend cross-link to sync counterpart
            if (src / "sync" / f"{name}.mdx").exists():
                content = f"> For the sync version, see [sync/{name}.md](../sync/{name}.md)\n\n" + content
            write_md(dst / "async" / f"{name}.md", content)

        # common/*.mdx -> *.md (directly in python-sdk/)
        for name, content in iter_sdk_mdx(src / "common"):
            write_md(dst / f"{name}.md", process_sdk_file(content, sdk, name))
    else:
        # Flat SDK: *.mdx -> *.md
        for name, content in iter_sdk_mdx(src):
            write_md(dst / f"{name}.md", process_sdk_file(content, sdk, name))


# ---------------------------------------------------------------------------
# Core Feature Docs (per-SDK with language tab extraction)
# ---------------------------------------------------------------------------

def generate_core_feature_docs():
    """Generate per-SDK feature docs from core docs with language tabs."""
    print("\n=== Core Feature Docs (per-SDK) ===")

    for feature in CORE_FEATURE_DOCS:
        src_path = DOCS_ROOT / f"{feature}.mdx"
        if not src_path.exists():
            print(f"  WARNING: {feature}.mdx not found, skipping")
            continue

        raw_content = read_mdx(src_path)
        if not raw_content:
            continue

        output_name = OUTPUT_NAME_OVERRIDES.get(feature, feature)

        # Check if the file actually has SDK language tabs
        has_sdk_tabs = False
        blocks = parse_tabs_blocks(raw_content)
        for _, _, sync_key, items in blocks:
            if sync_key == "language":
                labels = {label for label, _ in items}
                if labels & {"Python", "TypeScript", "Go", "Ruby"}:
                    has_sdk_tabs = True
                    break

        if not has_sdk_tabs:
            # This doc has syncKey="language" but no SDK tabs (e.g. Mac/Linux/Windows)
            # or no tabs at all - treat as platform doc
            print(f"  {feature}.mdx -> references/{output_name}.md (no SDK tabs)")
            content = process_content_common(raw_content)
            content = keep_all_tabs_as_markdown(content)
            content = resolve_links(content, None, "top")
            content = append_see_also_platform(content, feature)
            content = clean_content(content)
            write_md(OUTPUT_ROOT / f"{output_name}.md", content)
            continue

        # Generate per-SDK versions
        for sdk, label in SDK_LANGUAGES.items():
            content = process_content_common(raw_content)
            content = extract_language_tab(content, label)
            content = resolve_links(content, sdk, "sdk")
            content, api_ref_links = strip_cross_sdk_references(content, label)
            content = append_see_also_feature(content, sdk, feature,
                                              api_ref_links=api_ref_links)
            content = clean_content(content)

            dst = OUTPUT_ROOT / sdk / f"{output_name}.md"
            write_md(dst, content)


# ---------------------------------------------------------------------------
# Platform Docs (language-agnostic)
# ---------------------------------------------------------------------------

def generate_platform_docs():
    """Generate language-agnostic platform reference docs."""
    print("\n=== Platform Docs ===")

    for name in PLATFORM_DOCS:
        src_path = DOCS_ROOT / f"{name}.mdx"
        if not src_path.exists():
            print(f"  WARNING: {name}.mdx not found, skipping")
            continue

        content = read_mdx(src_path)
        if not content:
            continue

        content = process_content_common(content)
        content = keep_all_tabs_as_markdown(content)
        content = resolve_links(content, None, "platform")
        content, _ = strip_cross_sdk_references(content)
        content = append_see_also_platform(content, name)
        content = clean_content(content)
        write_md(PLATFORM_OUTPUT / f"{name}.md", content)


# ---------------------------------------------------------------------------
# CLI Reference
# ---------------------------------------------------------------------------

def generate_cli_reference():
    """Generate CLI reference from tools/cli.mdx."""
    print("\n=== CLI Reference ===")

    src_path = DOCS_ROOT / "tools" / "cli.mdx"
    if not src_path.exists():
        print("  WARNING: tools/cli.mdx not found, skipping")
        return

    content = read_mdx(src_path)
    if not content:
        return

    content = process_content_common(content)
    content = keep_all_tabs_as_markdown(content)
    content = resolve_links(content, None, "top")

    # Add See Also
    lines = ["\n\n## See Also\n"]
    for sdk in SDK_LANGUAGES:
        sdk_label = SDK_LANGUAGES[sdk]
        lines.append(f"- [{sdk_label} SDK](./{sdk}/README.md)")
    content = content.rstrip() + "\n".join(lines) + "\n"

    content = clean_content(content)
    write_md(OUTPUT_ROOT / "cli.md", content)


# ---------------------------------------------------------------------------
# REST API Reference Generation (from OpenAPI specs)
# ---------------------------------------------------------------------------

def load_openapi_spec(path: Path) -> dict:
    """Load and parse an OpenAPI JSON or YAML spec."""
    with open(path, "r", encoding="utf-8") as f:
        if path.suffix.lower() == ".json":
            return json.load(f)
        return yaml.safe_load(f)


def resolve_schema_ref(spec: dict, ref: str) -> tuple:
    """
    Resolve a $ref string one level deep.
    Returns (schema_name, schema_dict) or (None, None).
    """
    if not ref or not ref.startswith("#/components/schemas/"):
        return None, None
    name = ref.split("/")[-1]
    schema = spec.get("components", {}).get("schemas", {}).get(name)
    return name, schema


def schema_type_str(schema: dict, spec: dict = None) -> str:
    """Return a human-readable type string for a schema."""
    if not schema:
        return "object"
    if "$ref" in schema:
        name, _ = resolve_schema_ref(spec, schema["$ref"])
        return f"[{name}](#schema-{name.lower()})" if name else "object"
    t = schema.get("type", "object")
    if t == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            name, _ = resolve_schema_ref(spec, items["$ref"])
            inner = f"[{name}](#schema-{name.lower()})" if name else "object"
        else:
            inner = items.get("type", "object")
        return f"array of {inner}"
    fmt = schema.get("format")
    if fmt:
        return f"{t} ({fmt})"
    return t


def format_schema_properties(schema: dict, spec: dict) -> str:
    """Format schema properties as a markdown table."""
    if not schema:
        return ""
    props = schema.get("properties", {})
    if not props:
        # Could be an enum or simple type
        if "enum" in schema:
            vals = ", ".join(f"`{v}`" for v in schema["enum"])
            return f"Enum values: {vals}\n"
        return ""
    required = set(schema.get("required", []))
    lines = ["| Field | Type | Required | Description |",
             "|-------|------|----------|-------------|"]
    for pname, pschema in props.items():
        ptype = schema_type_str(pschema, spec)
        req = "Yes" if pname in required else "No"
        desc = pschema.get("description", "").replace("\n", " ").replace("|", "\\|")
        lines.append(f"| `{pname}` | {ptype} | {req} | {desc} |")
    return "\n".join(lines) + "\n"


def collect_endpoints_by_tag(spec: dict, skip_tags: set = None) -> dict:
    """
    Walk spec paths and group endpoints by tag.
    Returns {tag: [(method, path, operation), ...]}.
    """
    skip_tags = skip_tags or set()
    tag_map = {}
    for path, path_item in spec.get("paths", {}).items():
        for method in ("get", "post", "put", "patch", "delete"):
            op = path_item.get(method)
            if not op:
                continue
            tags = op.get("tags", ["untagged"])
            for tag in tags:
                if tag in skip_tags:
                    continue
                tag_map.setdefault(tag, []).append((method.upper(), path, op))
    return tag_map


def generate_api_tag_file(tag: str, endpoints: list, spec: dict,
                          spec_prefix: str, filename: str):
    """Generate a per-tag API reference markdown file."""
    lines = [f"# {tag.replace('-', ' ').title()} API\n"]

    for method, path, op in endpoints:
        summary = op.get("summary", "")
        description = op.get("description", "")
        anchor_path = path.lstrip("/")
        # Heading with anchor that matches link format: spec_prefix/tag/TAG/METHOD/path
        heading_anchor = f"{spec_prefix}/tag/{tag}/{method}/{anchor_path}"
        lines.append(f'## {method} `{path}` {{#{heading_anchor}}}\n')
        if summary:
            lines.append(f"**{summary}**\n")
        if description and description != summary:
            lines.append(f"{description}\n")

        # Parameters
        params = op.get("parameters", [])
        if params:
            lines.append("### Parameters\n")
            lines.append("| Name | In | Type | Required | Description |")
            lines.append("|------|-----|------|----------|-------------|")
            for p in params:
                pname = p.get("name", "")
                pin = p.get("in", "")
                pschema = p.get("schema", {})
                ptype = pschema.get("type", "string")
                fmt = pschema.get("format")
                if fmt:
                    ptype = f"{ptype} ({fmt})"
                req = "Yes" if p.get("required") else "No"
                desc = p.get("description", "").replace("\n", " ").replace("|", "\\|")
                lines.append(f"| `{pname}` | {pin} | {ptype} | {req} | {desc} |")
            lines.append("")

        # Request body
        req_body = op.get("requestBody")
        if req_body:
            lines.append("### Request Body\n")
            rb_desc = req_body.get("description", "")
            if rb_desc:
                lines.append(f"{rb_desc}\n")
            content = req_body.get("content", {})
            for content_type, media in content.items():
                schema = media.get("schema", {})
                if "$ref" in schema:
                    sname, sdef = resolve_schema_ref(spec, schema["$ref"])
                    if sname:
                        lines.append(f"Schema: **{sname}**\n")
                        if sdef:
                            lines.append(format_schema_properties(sdef, spec))
                elif schema.get("type") == "array" and "$ref" in schema.get("items", {}):
                    sname, sdef = resolve_schema_ref(spec, schema["items"]["$ref"])
                    if sname:
                        lines.append(f"Schema: array of **{sname}**\n")
                        if sdef:
                            lines.append(format_schema_properties(sdef, spec))
                else:
                    lines.append(format_schema_properties(schema, spec))

        # Responses
        responses = op.get("responses", {})
        if responses:
            lines.append("### Responses\n")
            lines.append("| Status | Description | Schema |")
            lines.append("|--------|-------------|--------|")
            for code, resp in sorted(responses.items()):
                desc = resp.get("description", "").replace("\n", " ").replace("|", "\\|")
                resp_schema = ""
                resp_content = resp.get("content", {})
                for ct, media in resp_content.items():
                    s = media.get("schema", {})
                    if "$ref" in s:
                        sname, _ = resolve_schema_ref(spec, s["$ref"])
                        if sname:
                            resp_schema = sname
                    elif s.get("type") == "array" and "$ref" in s.get("items", {}):
                        sname, _ = resolve_schema_ref(spec, s["items"]["$ref"])
                        if sname:
                            resp_schema = f"array of {sname}"
                    elif s.get("type"):
                        resp_schema = s["type"]
                lines.append(f"| {code} | {desc} | {resp_schema} |")
            lines.append("")

        lines.append("---\n")

    content = "\n".join(lines)
    write_md(API_OUTPUT / filename, content)


def generate_api_readme(main_tag_map: dict, toolbox_tag_map: dict,
                        main_spec: dict, toolbox_spec: dict):
    """Generate the API overview README.md."""
    lines = [
        "# Daytona API Reference\n",
        "## Base URL\n",
        "```",
        "https://app.daytona.io/api",
        "```\n",
        "## Authentication\n",
        "All API requests require a Bearer token in the `Authorization` header:\n",
        "```",
        "Authorization: Bearer <your-api-key>",
        "```\n",
        "See [Authentication](../../SKILL.md#authentication) for how to obtain an API key.\n",
        "---\n",
        "## Daytona API\n",
    ]

    # Main API table
    lines.append("| Method | Path | Summary | Tag |")
    lines.append("|--------|------|---------|-----|")
    for tag in sorted(main_tag_map.keys()):
        endpoints = main_tag_map[tag]
        tag_file = f"{tag}.md"
        for method, path, op in endpoints:
            summary = op.get("summary", "")
            anchor_path = path.lstrip("/")
            anchor = f"daytona/tag/{tag}/{method}/{anchor_path}"
            lines.append(
                f"| `{method}` | `{path}` | [{summary}](./{tag_file}#{anchor}) | [{tag}](./{tag_file}) |"
            )
    lines.append("")

    # Tag index with anchors matching link format: #daytona/tag/<tag>
    lines.append("### Tags\n")
    for tag in sorted(main_tag_map.keys()):
        tag_file = f"{tag}.md"
        count = len(main_tag_map[tag])
        lines.append(f'- [{tag}](./{tag_file}) ({count} endpoints) {{#daytona/tag/{tag}}}')
    lines.append("")

    # Toolbox API
    lines.append("---\n")
    lines.append("## Toolbox API {#daytona-toolbox}\n")
    lines.append("The Toolbox API runs inside sandboxes and provides file system, git, process, and other operations.\n")

    lines.append("| Method | Path | Summary | Tag |")
    lines.append("|--------|------|---------|-----|")
    for tag in sorted(toolbox_tag_map.keys()):
        endpoints = toolbox_tag_map[tag]
        tag_file = f"toolbox-{tag}.md"
        for method, path, op in endpoints:
            summary = op.get("summary", "")
            anchor_path = path.lstrip("/")
            anchor = f"daytona-toolbox/tag/{tag}/{method}/{anchor_path}"
            lines.append(
                f"| `{method}` | `{path}` | [{summary}](./{tag_file}#{anchor}) | [{tag}](./{tag_file}) |"
            )
    lines.append("")

    lines.append("### Tags\n")
    for tag in sorted(toolbox_tag_map.keys()):
        tag_file = f"toolbox-{tag}.md"
        count = len(toolbox_tag_map[tag])
        lines.append(f'- [{tag}](./{tag_file}) ({count} endpoints) {{#daytona-toolbox/tag/{tag}}}')
    lines.append("")

    content = "\n".join(lines)
    write_md(API_OUTPUT / "README.md", content)


def generate_api_reference():
    """Generate REST API reference docs from OpenAPI specs."""
    print("\n=== API Reference ===")

    if not MAIN_API_SPEC.exists():
        print(f"  WARNING: Main API spec not found at {MAIN_API_SPEC}, skipping")
        return
    if not TOOLBOX_API_SPEC.exists():
        print(f"  WARNING: Toolbox API spec not found at {TOOLBOX_API_SPEC}, skipping")
        return

    print(f"  Loading {MAIN_API_SPEC.name}...")
    main_spec = load_openapi_spec(MAIN_API_SPEC)
    print(f"  Loading {TOOLBOX_API_SPEC.name}...")
    toolbox_spec = load_openapi_spec(TOOLBOX_API_SPEC)

    # Collect endpoints grouped by tag
    main_tag_map = collect_endpoints_by_tag(main_spec, skip_tags=MAIN_API_SKIP_TAGS)
    toolbox_tag_map = collect_endpoints_by_tag(toolbox_spec)

    print(f"  Main API: {len(main_tag_map)} tags, "
          f"{sum(len(v) for v in main_tag_map.values())} endpoints")
    print(f"  Toolbox API: {len(toolbox_tag_map)} tags, "
          f"{sum(len(v) for v in toolbox_tag_map.values())} endpoints")

    # Generate per-tag files for main API
    for tag in sorted(main_tag_map.keys()):
        generate_api_tag_file(
            tag, main_tag_map[tag], main_spec,
            spec_prefix="daytona", filename=f"{tag}.md",
        )

    # Generate per-tag files for toolbox API (prefixed with toolbox-)
    for tag in sorted(toolbox_tag_map.keys()):
        generate_api_tag_file(
            tag, toolbox_tag_map[tag], toolbox_spec,
            spec_prefix="daytona-toolbox", filename=f"toolbox-{tag}.md",
        )

    # Generate overview README
    generate_api_readme(main_tag_map, toolbox_tag_map, main_spec, toolbox_spec)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"Daytona Skill Generator")
    print(f"  Source: {DOCS_ROOT}")
    print(f"  Output: {OUTPUT_ROOT}")

    # Clean output directory (but preserve SKILL.md at parent level)
    if OUTPUT_ROOT.exists():
        print(f"\nCleaning output directory: {OUTPUT_ROOT}")
        shutil.rmtree(OUTPUT_ROOT)
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    # 1. SDK API References
    for sdk in SDK_LANGUAGES:
        generate_sdk(sdk)

    # 2. Core Feature Docs (per-SDK)
    generate_core_feature_docs()

    # 3. Platform Docs
    generate_platform_docs()

    # 4. CLI Reference
    generate_cli_reference()

    # 5. REST API Reference
    generate_api_reference()

    print("\nDone!")

    # Summary
    md_files = list(OUTPUT_ROOT.rglob("*.md"))
    print(f"Generated {len(md_files)} files.")


if __name__ == "__main__":
    main()
