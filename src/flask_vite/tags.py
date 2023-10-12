from typing import Optional
import glob
from textwrap import dedent

from flask import current_app


def make_tag(static: bool = False, entry_point: Optional[str] = None):
    if static or not current_app.debug:
        return make_static_tag(entry_point)
    else:
        return make_debug_tag(entry_point)


def make_static_tag(entry_point: Optional[str]):
    js_files = glob.glob("vite/dist/assets/*.js")
    css_files = glob.glob("vite/dist/assets/*.css")

    js_file = js_files[0]
    css_file = css_files[0]
    if entry_point:
        js_file = next((f for f in js_files if _get_filename(f).startswith(entry_point)), None)
        css_file = next((f for f in css_files if _get_filename(f).startswith(entry_point)), None)

        if not js_file or not css_file:
            raise FileNotFoundError(f"No file was found for entrypoint: {entry_point}")

    return dedent(
        f"""
            <!-- FLASK_VITE_HEADER -->
            <script type="module" src="/_vite/{_get_filename(js_file)}"></script>
            <link rel="stylesheet" href="/_vite/{_get_filename(css_file)}"></link>
        """
    ).strip()


def make_debug_tag(entry_point: Optional[str]):
    return dedent(
        f"""
            <!-- FLASK_VITE_HEADER -->
            <script type="module" src="http://localhost:3000/@vite/client"></script>
            <script type="module" src="http://localhost:3000/{entry_point or 'main'}.js"></script>
        """
    ).strip()

def _get_filename(filepath: str) -> str: return filepath.split('/')[-1]
