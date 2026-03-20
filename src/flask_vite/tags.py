from typing import Optional
import glob
from textwrap import dedent
from pathlib import Path

from flask import current_app


def make_tag(static: bool = False, entry_point: Optional[str] = None):
    if static or not current_app.debug:
        return make_static_tag(entry_point)
    else:
        return make_debug_tag(entry_point)


def make_static_tag(entry_point: Optional[str]):
    js_file = css_file = None
    js_files = glob.glob("static/assets/js/*.js") or glob.glob("app/static/assets/js/*.js")
    css_files = glob.glob("static/assets/css/*.css") or glob.glob("app/static/assets/css/*.css")

    if css_files:
        css_file = css_files[0]
        if entry_point:
            css_file = next((f for f in css_files if _get_filename(f).startswith(entry_point)), None)

    if js_files:
        js_file = js_files[0]

        if entry_point:
            js_file = next((f for f in js_files if _get_filename(f).startswith(entry_point)), None)

    tags = ""
    if js_file:
        tags += dedent(
            f"""
                <script defer type="module" src="/assets/js/{_get_filename(js_file)}"></script>
            """
        )

    if css_file:
        tags += f'<link rel="stylesheet" href="/assets/css/{_get_filename(css_file)}"></link>'

    return tags.strip()


def make_debug_tag(entry_point: Optional[str]):
    filename = entry_point or 'main'

    search_dirs = [
        "vite",
        "vite/entrypoints/admin",
        "vite/entrypoints/frontend",
        "app/vite/entrypoints/admin",
        "app/vite/entrypoints/frontend",
    ]

    js_file = f"{filename}.js"
    for directory in search_dirs:
        fs_path = f"{directory}/{filename}.jsx"
        if Path(fs_path).exists():
            vite_root = "app/vite" if directory.startswith("app/vite") else "vite"
            js_file = fs_path[len(vite_root) + 1:]
            break

    return dedent(
        f"""
            <!-- FLASK_VITE_HEADER -->
            <script type="module" src="http://localhost:3000/@vite/client"></script>
            <script type="module" src="http://localhost:3000/{js_file}"></script>
        """
    ).strip()

def _get_filename(filepath: str) -> str: return filepath.split('/')[-1]
