# WORM-Library Notebook Testing

This document describes the automated testing system for WORM-Library Jupyter notebooks.

## Overview

WORM-Library uses a **two-tier testing approach**:

### Tier 1: Fast Syntax Testing (test_notebooks.py)
- **What**: Validates Python syntax and image URLs without executing code
- **Speed**: < 1 minute for all notebooks
- **When**: Runs on every push and pull request
- **Purpose**: Fast feedback, catches syntax errors and broken links

Checks:
1. **Python syntax errors** - Ensures all code cells have valid Python syntax
2. **Broken image links** - Validates that hotlinked images are accessible

### Tier 2: Full Execution Testing (execute_notebooks.py)
- **What**: Executes all notebooks to catch runtime errors
- **Speed**: ~10-60 minutes (depends on notebook complexity)
- **When**: Runs weekly or on-demand
- **Purpose**: Catches breaking changes in dependencies (aqequil, pychnosz, etc.)

Checks:
1. **Runtime errors** - Detects errors from package updates or breaking API changes
2. **Dependency issues** - Ensures all required packages and data files are available
3. **Execution completion** - Verifies notebooks run to completion without hanging

## Quick Start

### Tier 1: Fast Syntax Testing

Run syntax and link validation (no execution):

```bash
python test_notebooks.py
```

Run on a specific directory:

```bash
python test_notebooks.py /path/to/notebooks
```

From a Jupyter notebook:

```python
from test_notebooks import main
main('.')  # Run in current directory
```

### Tier 2: Full Execution Testing

**Prerequisites**: Requires eq3_6, aqequil, pychnosz, and other dependencies installed.

Execute all notebooks with default 10-minute timeout per notebook:

```bash
python execute_notebooks.py
```

Execute with custom timeout (in seconds):

```bash
python execute_notebooks.py . 1200  # 20 minute timeout per notebook
```

From a Jupyter notebook:

```python
from execute_notebooks import main
main('.', timeout=1200)  # 20 minute timeout
```

**Note**: Execution testing can take a long time (30-60+ minutes for all notebooks).

## What Gets Tested

The test script automatically:
- ✅ Scans all `.ipynb` files in the repository
- ✅ Excludes specific folders: `WORKSHOP`, `WORM-Development`, `WORM-Tour`
- ✅ Excludes specific notebooks: `WORM-Library.ipynb`
- ✅ Checks Python syntax in all code cells
- ✅ Validates HTTP/HTTPS image URLs in markdown cells
- ✅ Caches URL checks to avoid redundant requests

## Automated Testing (GitHub Actions)

### Three Workflows

#### 1. Build Docker Image (`build-docker-image.yml`)
Builds a Docker container with eq3_6 and all dependencies.

**Runs:**
- When `Dockerfile` changes
- Weekly on Mondays at 3 AM UTC (to get latest package updates)
- Manually via GitHub Actions

**Publishes to:** GitHub Container Registry (ghcr.io)

#### 2. Fast Syntax Tests (`test-notebooks.yml`)
Validates Python syntax and image URLs without executing notebooks.

**Runs:**
- On every push to any branch
- On every pull request
- Weekly on Mondays at 9 AM UTC (to catch link rot)
- Manually via GitHub Actions

**Tests against:** Python versions 3.9, 3.10, 3.11, 3.12, and 3.13

**Duration:** ~1 minute

#### 3. Full Execution Tests (`execute-notebooks.yml`)
Executes all notebooks using the Docker container to catch runtime errors.

**Runs:**
- Weekly on Tuesdays at 10 AM UTC (after Docker image builds)
- Manually via GitHub Actions (with configurable timeout)

**Environment:** Docker container with eq3_6, aqequil, pychnosz, etc.

**Duration:** ~30-60 minutes (depends on notebooks)

## Test Output

### Successful test:
```
Testing: 1-Introduction/1-Introduction.ipynb
  ✅ All checks passed
```

### Syntax error:
```
Testing: path/to/notebook.ipynb
  ❌ Cell 45: Syntax error at line 1: invalid syntax
```

### Broken image link:
```
Testing: path/to/notebook.ipynb
  ⚠️  Cell 47: Broken image link - https://example.com/image.jpg (HTTP 404)
```

## Exit Codes

- `0` - All tests passed
- `1` - Syntax errors found (fails build)

**Note:** Broken image links generate warnings but do not fail the build, since external links may be temporarily unavailable.

## Configuration

Edit `test_notebooks.py` to customize:

```python
# Folders to exclude
EXCLUDE_FOLDERS = ['WORKSHOP', 'WORM-Development', 'WORM-Tour', '.ipynb_checkpoints', '.git']

# Notebooks to exclude
EXCLUDE_NOTEBOOKS = ['WORM-Library.ipynb']

# URL check timeout (seconds)
IMAGE_TIMEOUT = 10
```

## How Syntax Checking Works

The test script validates Python syntax using Python's built-in AST parser. Before checking, it automatically filters out Jupyter-specific syntax that isn't valid Python:

- **Line and cell magics**: Commands starting with `%` or `%%` (e.g., `%matplotlib inline`, `%%bash`)
- **IPython help operators**: Lines like `object?` or `object??` used to display documentation

The script intelligently distinguishes between help operators and question marks in comments or strings, so code like `# What does this do?` won't be incorrectly filtered.

## Troubleshooting

### False positives for syntax errors

If you see syntax errors reported for valid Python code, this may indicate:
- Use of experimental Python syntax not yet supported by the AST parser
- Malformed code that works in Jupyter due to auto-completion but isn't valid Python
- Edge cases with Jupyter magic detection (please report these as issues)

### Broken image links

If image links are reported as broken but work in your browser:
- The server may be blocking automated requests
- The URL may require authentication
- There may be temporary network issues

Verify the link manually and consider:
- Hosting images in the repository instead
- Using more reliable image hosting services
- Adding the URL to an ignore list (requires modifying the script)

## Docker Container Setup

The execution testing workflow uses a Docker container with all dependencies pre-installed.

### What's Included

The `Dockerfile` installs:
- **eq3_6**: Compiled from source (https://github.com/39alpha/eq3_6)
- **Python packages**: aqequil, pychnosz, aqorg, complicator, propfit
- **Scientific stack**: numpy, pandas, matplotlib, scipy
- **Jupyter**: jupyter, jupyterlab, papermill, nbconvert

### Customizing the Container

Edit `Dockerfile` to:
- Change Python version
- Add/remove packages
- Modify eq3_6 build options
- Set different environment variables

After editing, the container will automatically rebuild:
- When you push changes to `Dockerfile`
- Weekly (to get latest package updates)
- Manually via GitHub Actions

### Using the Container Locally

Pull and use the pre-built container:

```bash
# Pull from GitHub Container Registry
docker pull ghcr.io/YOUR-USERNAME/worm-library/worm-test:latest

# Run tests in the container
docker run --rm -v $(pwd):/workspace -w /workspace \
  ghcr.io/YOUR-USERNAME/worm-library/worm-test:latest \
  python execute_notebooks.py
```

Or build locally:

```bash
# Build the container
docker build -t worm-test .

# Run execution tests
docker run --rm -v $(pwd):/workspace -w /workspace \
  worm-test python execute_notebooks.py
```

## Execution Testing Configuration

Edit `execute_notebooks.py` to customize:

```python
# Folders to exclude
EXCLUDE_FOLDERS = ['WORKSHOP', 'WORM-Development', 'WORM-Tour', '.ipynb_checkpoints', '.git']

# Notebooks to exclude
EXCLUDE_NOTEBOOKS = ['WORM-Library.ipynb']

# Default timeout per notebook (seconds)
DEFAULT_TIMEOUT = 600  # 10 minutes

# Continue testing even if some notebooks fail
CONTINUE_ON_ERROR = True
```

## Troubleshooting Execution Tests

### Timeout Errors

If a notebook times out during execution:
- Increase timeout: `python execute_notebooks.py . 1200` (20 minutes)
- Or edit `DEFAULT_TIMEOUT` in `execute_notebooks.py`
- Or skip that notebook by adding to `EXCLUDE_NOTEBOOKS`

### Missing Dependencies

If execution fails due to missing packages:
- Update `Dockerfile` to install the package
- Push changes to trigger container rebuild
- Wait for rebuild, then re-run execution tests

### Data File Issues

If notebooks fail because they can't find data files:
- Ensure data files are committed to the repository
- Check that paths in notebooks are relative to repository root
- Update notebooks to use correct paths

## Maintenance

### Weekly Automated Tasks

- **Monday 3 AM**: Docker image rebuilds (gets latest package versions)
- **Monday 9 AM**: Syntax tests run (catches link rot)
- **Tuesday 10 AM**: Execution tests run (catches runtime errors with updated packages)

### When to Run Manual Tests

Run manual execution tests:
- Before major releases
- After updating dependencies
- When you suspect a package update broke something
- To verify fixes for reported issues
