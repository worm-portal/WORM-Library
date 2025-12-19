#!/usr/bin/env python3
"""
Test script for WORM-Library Jupyter notebooks.
Checks for:
1. Python syntax errors
2. Broken hotlinked images
"""

import json
import os
import sys
import ast
import re
from pathlib import Path
from typing import List, Tuple, Dict
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed


# Configuration
EXCLUDE_FOLDERS = ['WORM-Development', 'WORM-Tour', '.ipynb_checkpoints', '.git']
EXCLUDE_NOTEBOOKS = ['WORM-Library.ipynb',
                     '3-breakout_lab-grown_microbe.ipynb', # breakout session notebook/assignment
                     '4-breakout_marine_vent_energy.ipynb', # breakout session notebook/assignment
                     '5-breakout_bioremediation.ipynb', # breakout session notebook/assignment
                    ]
# Match markdown images: ![alt](url) or ![alt](url "title")
# Capture only the URL, stopping at space (if title present) or closing paren
IMAGE_URL_PATTERN = re.compile(r'!\[.*?\]\((https?://[^\s\)]+)')
IMAGE_TIMEOUT = 10  # seconds


class NotebookTester:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.errors = []
        self.warnings = []
        self.checked_urls = {}  # Cache for URL checks

    def should_skip_path(self, path: Path) -> bool:
        """Check if path should be skipped based on exclude rules."""
        parts = path.parts
        for exclude in EXCLUDE_FOLDERS:
            if exclude in parts:
                return True
        if path.name in EXCLUDE_NOTEBOOKS:
            return True
        return False

    def find_notebooks(self) -> List[Path]:
        """Find all notebooks that should be tested."""
        notebooks = []
        for nb_path in self.root_dir.rglob('*.ipynb'):
            if not self.should_skip_path(nb_path):
                notebooks.append(nb_path)
        return sorted(notebooks)

    def filter_jupyter_syntax(self, code: str) -> str:
        """
        Filter out Jupyter-specific syntax that isn't valid Python.
        This includes magic commands and IPython help operators.
        """
        lines = code.split('\n')
        filtered_lines = []

        for line in lines:
            stripped = line.strip()

            # Skip IPython magic commands (line and cell magics)
            if stripped.startswith('%'):
                continue

            # Skip IPython help operator lines
            # But ignore ? in comments (after #) or in strings
            # Simple heuristic: check if ? appears before any # comment
            if stripped.endswith('?') or stripped.endswith('??'):
                # Check if the ? is in a comment
                comment_pos = stripped.find('#')
                if comment_pos == -1:
                    # No comment, check if this looks like a help operator
                    # Valid: "object?", "object.method?", "module.Class?"
                    # Invalid: part of a string
                    # Simple check: if line has only word characters, dots, and ? at end
                    # This is a help operator line
                    if stripped.endswith('??'):
                        test_str = stripped[:-2].strip()
                    else:
                        test_str = stripped[:-1].strip()
                    # If what's left looks like a valid identifier/attribute access
                    if test_str and not any(c in test_str for c in ' ()[]{},"\''):
                        # Looks like a help operator, skip it
                        continue
                # If ? is in a comment or doesn't match help pattern, keep the line

            # Keep the line
            filtered_lines.append(line)

        return '\n'.join(filtered_lines)

    def check_python_syntax(self, notebook_path: Path) -> List[str]:
        """Check Python code cells for syntax errors."""
        errors = []

        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
        except json.JSONDecodeError as e:
            return [f"Invalid JSON format: {e}"]
        except Exception as e:
            return [f"Failed to read notebook: {e}"]

        cells = notebook.get('cells', [])

        for cell_idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'code':
                source = cell.get('source', [])
                # Join source lines into a single string
                if isinstance(source, list):
                    code = ''.join(source)
                else:
                    code = source

                # Skip empty cells
                if not code.strip():
                    continue

                # Filter out Jupyter-specific syntax
                filtered_code = self.filter_jupyter_syntax(code)

                # Skip if filtering removed everything
                if not filtered_code.strip():
                    continue

                # Try to parse the code
                try:
                    ast.parse(filtered_code)
                except SyntaxError as e:
                    errors.append(
                        f"Cell {cell_idx + 1}: Syntax error at line {e.lineno}: {e.msg}"
                    )
                except Exception as e:
                    errors.append(
                        f"Cell {cell_idx + 1}: Parse error: {e}"
                    )

        return errors

    def extract_image_urls(self, notebook_path: Path) -> List[Tuple[int, str]]:
        """Extract image URLs from markdown cells."""
        urls = []

        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
        except Exception:
            return urls

        cells = notebook.get('cells', [])

        for cell_idx, cell in enumerate(cells):
            if cell.get('cell_type') == 'markdown':
                source = cell.get('source', [])
                # Join source lines into a single string
                if isinstance(source, list):
                    markdown = ''.join(source)
                else:
                    markdown = source

                # Find all image URLs
                matches = IMAGE_URL_PATTERN.findall(markdown)
                for url in matches:
                    urls.append((cell_idx + 1, url))

        return urls

    def check_url(self, url: str) -> Tuple[bool, str]:
        """Check if a URL is accessible."""
        # Use cache to avoid checking the same URL multiple times
        if url in self.checked_urls:
            return self.checked_urls[url]

        try:
            # Add a user agent to avoid being blocked
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (WORM-Library Notebook Tester)'}
            )
            with urllib.request.urlopen(req, timeout=IMAGE_TIMEOUT) as response:
                if response.status == 200:
                    result = (True, "OK")
                else:
                    result = (False, f"HTTP {response.status}")
        except urllib.error.HTTPError as e:
            result = (False, f"HTTP {e.code}")
        except urllib.error.URLError as e:
            result = (False, f"URL Error: {e.reason}")
        except Exception as e:
            result = (False, f"Error: {str(e)}")

        self.checked_urls[url] = result
        return result

    def check_image_urls(self, notebook_path: Path) -> List[str]:
        """Check all image URLs in a notebook."""
        errors = []
        urls = self.extract_image_urls(notebook_path)

        if not urls:
            return errors

        # Check URLs in parallel for efficiency
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {
                executor.submit(self.check_url, url): (cell_idx, url)
                for cell_idx, url in urls
            }

            for future in as_completed(future_to_url):
                cell_idx, url = future_to_url[future]
                is_ok, message = future.result()

                if not is_ok:
                    errors.append(
                        f"Cell {cell_idx}: Broken image link - {url} ({message})"
                    )

        return errors

    def test_notebook(self, notebook_path: Path) -> Dict:
        """Test a single notebook."""
        rel_path = notebook_path.relative_to(self.root_dir)

        result = {
            'path': str(rel_path),
            'syntax_errors': [],
            'image_errors': []
        }

        print(f"Testing: {rel_path}")

        # Check Python syntax
        syntax_errors = self.check_python_syntax(notebook_path)
        if syntax_errors:
            result['syntax_errors'] = syntax_errors
            for error in syntax_errors:
                print(f"  ❌ {error}")

        # Check image URLs
        image_errors = self.check_image_urls(notebook_path)
        if image_errors:
            result['image_errors'] = image_errors
            for error in image_errors:
                print(f"  ⚠️  {error}")

        if not syntax_errors and not image_errors:
            print(f"  ✅ All checks passed")

        return result

    def run_tests(self) -> int:
        """Run all tests and return exit code."""
        print("=" * 70)
        print("WORM-Library Notebook Testing")
        print("=" * 70)
        print(f"\nRoot directory: {self.root_dir}")
        print(f"Excluded folders: {', '.join(EXCLUDE_FOLDERS)}")
        print(f"Excluded notebooks: {', '.join(EXCLUDE_NOTEBOOKS)}")
        print()

        notebooks = self.find_notebooks()
        print(f"Found {len(notebooks)} notebooks to test\n")

        if not notebooks:
            print("No notebooks found!")
            return 1

        results = []
        for notebook in notebooks:
            result = self.test_notebook(notebook)
            results.append(result)
            print()

        # Summary
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        total_syntax_errors = sum(len(r['syntax_errors']) for r in results)
        total_image_errors = sum(len(r['image_errors']) for r in results)
        notebooks_with_syntax_errors = sum(1 for r in results if r['syntax_errors'])
        notebooks_with_image_errors = sum(1 for r in results if r['image_errors'])

        print(f"\nTotal notebooks tested: {len(notebooks)}")
        print(f"Notebooks with syntax errors: {notebooks_with_syntax_errors}")
        print(f"Total syntax errors: {total_syntax_errors}")
        print(f"Notebooks with broken images: {notebooks_with_image_errors}")
        print(f"Total broken images: {total_image_errors}")

        if total_syntax_errors > 0:
            print("\n⚠️  FAILED: Found Python syntax errors")
            return 1

        if total_image_errors > 0:
            print("\n⚠️  WARNING: Found broken image links (not failing build)")
            # Don't fail on broken images, just warn

        if total_syntax_errors == 0 and total_image_errors == 0:
            print("\n✅ SUCCESS: All tests passed!")

        return 0 if total_syntax_errors == 0 else 1


def main(root_dir=None):
    """
    Main entry point.

    Parameters
    ----------
    root_dir : str, optional
        Root directory to search for notebooks. If None, will use command-line
        argument or current directory. When calling from a Jupyter notebook,
        pass root_dir='.' explicitly to avoid issues with sys.argv.
    """
    # Determine root directory
    if root_dir is None:
        # Check if we have a command-line argument and if it's valid
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            # Ignore Jupyter kernel arguments (start with -)
            if not arg.startswith('-'):
                root_dir = arg
            else:
                root_dir = '.'
        else:
            root_dir = '.'

    tester = NotebookTester(root_dir)
    exit_code = tester.run_tests()

    # Only call sys.exit if running as script (not in notebook)
    # Check if we're in IPython/Jupyter
    try:
        __IPYTHON__
        in_notebook = True
    except NameError:
        in_notebook = False

    if not in_notebook:
        sys.exit(exit_code)

    return exit_code


if __name__ == '__main__':
    main()
