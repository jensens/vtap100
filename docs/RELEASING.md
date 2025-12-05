# Release Process

This project uses GitHub Releases with PyPI Trusted Publishing for automated releases.

## Version Management

The version is automatically derived from Git tags using `hatch-vcs`:

- Tags like `v0.5.0`, `v1.0.0`, `v2.1.3` become release versions
- Development versions show as `v0.5.0.dev12` (12 commits after 0.5.0)
- Pre-releases: `v1.0.0a1`, `v1.0.0b2`, `v1.0.0rc1`

## Creating a Release

1. Ensure all changes are merged to `main` and CI is green
2. Go to [GitHub Releases](https://github.com/jensens/vtap100/releases)
3. Click "Draft a new release"
4. Click "Choose a tag" and **type a new tag** (e.g., `v0.5.0`, `v1.0.0a1`)
5. Select "Create new tag on publish"
6. Target: `main` branch
7. Generate release notes or write them manually
8. Click "Publish release"

The release workflow will automatically:
- Run all tests
- Build the package with `build-and-inspect-python-package`
- Upload to PyPI using Trusted Publishing

## Test PyPI

Every push to `main` automatically uploads a development version to [Test PyPI](https://test.pypi.org/project/vtap100/).

Install from Test PyPI:

```bash
pip install -i https://test.pypi.org/simple/ vtap100
```

## Required GitHub Configuration

### Environments

Two GitHub environments must be configured:

1. **release-test-pypi**: For Test PyPI uploads (automatic on main)
2. **release-pypi**: For production PyPI uploads (on GitHub Release)

### PyPI Trusted Publishing

Configure Trusted Publishing on PyPI:
1. Go to https://pypi.org/manage/project/vtap100/settings/publishing/
2. Add a new publisher:
   - Owner: `jensens`
   - Repository: `vtap100`
   - Workflow: `release.yaml`
   - Environment: `release-pypi`

Same for Test PyPI at https://test.pypi.org/manage/project/vtap100/settings/publishing/
with environment `release-test-pypi`.

## Troubleshooting

### Version shows as `0.0.0.dev0`

The `_version.py` file is not generated. Run:

```bash
uv sync  # or pip install -e .
```

### Package not uploading

Check that:
1. GitHub environments are configured
2. PyPI Trusted Publishing is set up correctly
3. The workflow has `id-token: write` permission
