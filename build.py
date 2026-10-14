"""Build the site: turn content/ into docs/, the folder GitHub Pages serves."""

import html
import re
import shutil
from datetime import date
from pathlib import Path

import markdown

SITE_NAME = "Brendan D'Aquino"

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
OUTPUT = ROOT / "docs"

# $$...$$ (may span lines) or $...$ (single line)
MATH = re.compile(r"\$\$.+?\$\$|\$[^$\n]+\$", re.DOTALL)


def split_front_matter(text):
    """Split "---\\nkey: value\\n---\\nbody" into ({"key": "value"}, "body")."""
    meta = {}
    if text.startswith("---\n"):
        header, text = text[4:].split("\n---\n", 1)
        for line in header.splitlines():
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text


def markdown_to_html(text):
    """Convert Markdown to HTML without letting Markdown touch the LaTeX."""
    # Markdown would mangle LaTeX (\{ becomes {, \\ becomes \, *a* becomes
    # italics), so swap each piece of math for a placeholder, convert, and
    # put the math back afterwards.
    stash = []

    def hide(match):
        stash.append(match.group(0))
        return f"MATH{len(stash) - 1}END"

    text = MATH.sub(hide, text)
    out = markdown.markdown(text, extensions=["fenced_code", "footnotes", "tables"])
    for i, math in enumerate(stash):
        out = out.replace(f"MATH{i}END", html.escape(math, quote=False))
    return out


def render(title, content, math=False):
    """Fill in the blanks in templates/base.html."""
    page = (TEMPLATES / "base.html").read_text()
    head = (TEMPLATES / "math.html").read_text() if math else ""
    page = page.replace("{{ title }}", html.escape(title, quote=False))
    page = page.replace("{{ head }}", head)
    return page.replace("{{ content }}", content)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d:%B} {d.day}, {d.year}"


def build():
    # Start from an empty docs/ so deleted posts don't linger
    shutil.rmtree(OUTPUT, ignore_errors=True)
    posts = []

    for src in sorted(CONTENT.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(CONTENT)

        # Anything that isn't Markdown (CSS, images, CNAME) is copied as-is
        if src.suffix != ".md":
            (OUTPUT / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src, OUTPUT / rel)
            continue

        meta, body = split_front_matter(src.read_text())
        content = markdown_to_html(body)

        # A page with a date is a blog post: add the title and date on top
        if "date" in meta:
            content = (
                f"<article>\n<h1>{meta['title']}</h1>\n"
                f'<time datetime="{meta["date"]}">{nice_date(meta["date"])}</time>\n'
                f"{content}\n</article>"
            )
            posts.append(meta | {"url": f"/{rel.parent.as_posix()}/"})

        title = f"{meta['title']} · {SITE_NAME}" if "title" in meta else SITE_NAME
        math = meta.get("math") == "true"
        write(OUTPUT / rel.with_suffix(".html"), render(title, content, math))

    # The blog index lists every post, newest first
    posts.sort(key=lambda p: p["date"], reverse=True)
    items = "\n".join(
        f'<li><time datetime="{p["date"]}">{p["date"]}</time> '
        f'<a href="{p["url"]}">{p["title"]}</a></li>'
        for p in posts
    )
    content = f'<h1>Blog</h1>\n<ul class="post-list">\n{items}\n</ul>'
    write(OUTPUT / "blog" / "index.html", render(f"Blog · {SITE_NAME}", content))

    print(f"Built {len(posts)} posts into {OUTPUT.name}/")


if __name__ == "__main__":
    build()