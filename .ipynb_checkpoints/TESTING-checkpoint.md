# WORM-Library Notebook Testing

This document describes the automated testing system for WORM-Library Jupyter notebooks.

## Overview

The testing system checks all notebooks for:
1. **Python syntax errors** - Ensures all code cells have valid Python syntax
2. **Broken image links** - Validates that hotlinked images are accessible

## Quick Start

### Run tests locally

```bash
python test_notebooks.py
```

### Run tests on a specific directory

```bash
python test_notebooks.py /path/to/notebooks
```

## What Gets Tested

The test script automatically:
- ✅ Scans all `.ipynb` files in the repository
- ✅ Excludes specific folders: `WORKSHOP`, `WORM-Development`, `WORM-Tour`
- ✅ Excludes specific notebooks: `WORM-Library.ipynb`
- ✅ Checks Python syntax in all code cells
- ✅ Validates HTTP/HTTPS image URLs in markdown cells
- ✅ Caches URL checks to avoid redundant requests

## Automated Testing (GitHub Actions)

Tests run automatically:
- **On every push** to any branch
- **On every pull request**
- **Weekly on Mondays at 9 AM UTC** (to catch link rot over time)
- **Manually** via GitHub Actions interface

The workflow tests against Python versions: 3.9, 3.10, and 3.11

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

## Troubleshooting

### False positives for syntax errors

Some Jupyter magic commands (like `%%bash`) may be flagged as syntax errors. This is expected behavior since the test script only validates standard Python syntax, not Jupyter-specific extensions.

### Broken image links

If image links are reported as broken but work in your browser:
- The server may be blocking automated requests
- The URL may require authentication
- There may be temporary network issues

Verify the link manually and consider:
- Hosting images in the repository instead
- Using more reliable image hosting services
- Adding the URL to an ignore list (requires modifying the script)

## Future Enhancements

Potential additions to the testing system:
- Full notebook execution testing (currently only checks syntax)
- Cell output validation
- Dependency checking
- Performance benchmarking
- Custom ignore patterns for known issues
