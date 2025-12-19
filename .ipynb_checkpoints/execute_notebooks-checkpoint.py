#!/usr/bin/env python3
"""
Execution testing script for WORM-Library Jupyter notebooks.
Uses papermill to execute notebooks and detect runtime errors.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Dict
import papermill as pm
from datetime import datetime


# Configuration
EXCLUDE_FOLDERS = ['WORKSHOP', 'WORM-Development', 'WORM-Tour', '.ipynb_checkpoints', '.git']
EXCLUDE_NOTEBOOKS = ['WORM-Library.ipynb',
                     '3-breakout_lab-grown_microbe.ipynb', # breakout session notebook/assignment
                     '4-breakout_marine_vent_energy.ipynb', # breakout session notebook/assignment
                     '5-breakout_bioremediation.ipynb', # breakout session notebook/assignment
                    ]
DEFAULT_TIMEOUT = 600  # 10 minutes per notebook
CONTINUE_ON_ERROR = True  # Keep testing even if some notebooks fail


class NotebookExecutor:
    def __init__(self, root_dir: str, timeout: int = DEFAULT_TIMEOUT):
        self.root_dir = Path(root_dir)
        self.timeout = timeout
        self.results = []

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

    def execute_notebook(self, notebook_path: Path) -> Dict:
        """Execute a single notebook using papermill."""
        rel_path = notebook_path.relative_to(self.root_dir)

        result = {
            'path': str(rel_path),
            'status': 'unknown',
            'error': None,
            'execution_time': None
        }

        print(f"Executing: {rel_path}")

        # Create temporary output file
        with tempfile.NamedTemporaryFile(suffix='.ipynb', delete=False) as tmp:
            output_path = tmp.name

        # Save original working directory
        original_cwd = os.getcwd()

        try:
            start_time = datetime.now()

            # Change to notebook's directory so all file operations use correct paths
            notebook_dir = notebook_path.parent.resolve()
            os.chdir(notebook_dir)

            # Execute notebook with papermill
            # Use notebook filename (not full path) since we're in its directory
            pm.execute_notebook(
                notebook_path.name,
                output_path,
                kernel_name='python3',
                timeout=self.timeout,
                progress_bar=False
            )

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()

            result['status'] = 'success'
            result['execution_time'] = execution_time
            print(f"  ✅ Success ({execution_time:.1f}s)")

        except pm.PapermillExecutionError as e:
            result['status'] = 'execution_error'
            result['error'] = str(e)
            print(f"  ❌ Execution error: {e}")

        except TimeoutError as e:
            result['status'] = 'timeout'
            result['error'] = f"Timeout after {self.timeout}s"
            print(f"  ⏱️  Timeout after {self.timeout}s")

        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f"  ❌ Error: {e}")

        finally:
            # Always restore original working directory
            os.chdir(original_cwd)

            # Clean up temporary file
            try:
                os.unlink(output_path)
            except:
                pass

        return result

    def run_tests(self) -> int:
        """Run execution tests on all notebooks and return exit code."""
        print("=" * 70)
        print("WORM-Library Notebook Execution Testing")
        print("=" * 70)
        print(f"\nRoot directory: {self.root_dir}")
        print(f"Excluded folders: {', '.join(EXCLUDE_FOLDERS)}")
        print(f"Excluded notebooks: {', '.join(EXCLUDE_NOTEBOOKS)}")
        print(f"Timeout per notebook: {self.timeout}s")
        print(f"Continue on error: {CONTINUE_ON_ERROR}")
        print()

        notebooks = self.find_notebooks()
        print(f"Found {len(notebooks)} notebooks to execute\n")

        if not notebooks:
            print("No notebooks found!")
            return 1

        # Execute all notebooks
        for notebook in notebooks:
            result = self.execute_notebook(notebook)
            self.results.append(result)
            print()

            # Stop on first error if CONTINUE_ON_ERROR is False
            if not CONTINUE_ON_ERROR and result['status'] != 'success':
                print("Stopping due to error (CONTINUE_ON_ERROR=False)")
                break

        # Summary
        print("=" * 70)
        print("EXECUTION TEST SUMMARY")
        print("=" * 70)

        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'success')
        failed = sum(1 for r in self.results if r['status'] == 'execution_error')
        timeout = sum(1 for r in self.results if r['status'] == 'timeout')
        errors = sum(1 for r in self.results if r['status'] == 'error')

        print(f"\nTotal notebooks tested: {total}")
        print(f"Successful: {success}")
        print(f"Execution errors: {failed}")
        print(f"Timeouts: {timeout}")
        print(f"Other errors: {errors}")

        # Show failed notebooks
        if failed > 0:
            print("\nNotebooks with execution errors:")
            for result in self.results:
                if result['status'] == 'execution_error':
                    print(f"  - {result['path']}")
                    if result['error']:
                        # Show first line of error
                        error_lines = result['error'].split('\n')
                        print(f"    {error_lines[0][:100]}")

        # Total execution time
        total_time = sum(r['execution_time'] for r in self.results if r['execution_time'])
        print(f"\nTotal execution time: {total_time:.1f}s ({total_time/60:.1f} minutes)")

        if success == total:
            print("\n✅ SUCCESS: All notebooks executed without errors!")
            return 0
        else:
            print(f"\n⚠️  FAILED: {failed + timeout + errors} notebook(s) failed")
            return 1


def main(root_dir=None, timeout=DEFAULT_TIMEOUT):
    """
    Main entry point.

    Parameters
    ----------
    root_dir : str, optional
        Root directory to search for notebooks. If None, will use command-line
        argument or current directory.
    timeout : int, optional
        Timeout in seconds for each notebook execution. Default is 600 (10 min).
    """
    # Determine root directory
    if root_dir is None:
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if not arg.startswith('-'):
                root_dir = arg
            else:
                root_dir = '.'
        else:
            root_dir = '.'

    # Check if timeout is specified
    if len(sys.argv) > 2 and sys.argv[2].isdigit():
        timeout = int(sys.argv[2])

    executor = NotebookExecutor(root_dir, timeout=timeout)
    exit_code = executor.run_tests()

    # Only call sys.exit if running as script (not in notebook)
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
