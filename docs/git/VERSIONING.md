# Version Control Strategy

## Version Numbering

**Current Version:** `v0.1.0` (SETUP-001 Complete - Project Structure Foundation)

### Semantic Versioning (SemVer)

We use **Semantic Versioning** format: `MAJOR.MINOR.PATCH`

- **MAJOR** (X.0.0): Breaking changes or major milestones
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, small improvements

### Version Strategy for Zema AI

#### Phase 0: Project Setup (v0.1.0 - v0.9.0)
- **v0.1.0**: ✅ SETUP-001 - Project Structure Foundation
- **v0.2.0**: SETUP-002 - Configuration System
- **v0.3.0**: SETUP-003 - Logging System
- **v0.4.0**: Hardware verification (camera, audio)
- **v0.5.0**: Voice module (STT, TTS, wake word)
- **v0.6.0**: Vision module (camera, PTZ, gestures)
- **v0.7.0**: AI module (LLM client, context)
- **v0.8.0**: API server and dashboard
- **v0.9.0**: Integration and testing

#### Phase 1: Beta Release (v1.0.0)
- **v1.0.0**: First stable release with core features working

#### Phase 2: Stable Releases (v1.1.0+)
- **v1.1.0**: New features
- **v1.2.0**: More features
- **v2.0.0**: Major rewrite or breaking changes

---

## Current Milestone Tags

### v0.1.0 - Project Structure Foundation ✅
**Tag:** `v0.1.0`  
**Created:** SETUP-001 Complete  
**Description:** Complete project structure with all directories, files, and configuration  
**What's Included:**
- ✅ Complete directory structure (26 directories)
- ✅ All __init__.py files (15 files)
- ✅ All root files (README.md, requirements.txt, pyproject.toml, .env.example, .gitignore)
- ✅ Configuration system foundation
- ✅ Logging system foundation
- ✅ Documentation structure

**To Revert to This State:**
```bash
git checkout v0.1.0
# Or create a new branch from this tag
git checkout -b restore-v0.1.0 v0.1.0
```

---

## Tagging Best Practices

### When to Create Tags

1. **Milestone Completion** - After completing major setup steps
2. **Feature Completion** - After completing major features
3. **Release Candidates** - Before stable releases
4. **Stable Releases** - Production-ready versions

### Tag Naming Convention

- **Format:** `vMAJOR.MINOR.PATCH`
- **Examples:**
  - `v0.1.0` - Project structure milestone
  - `v0.2.0` - Configuration system milestone
  - `v1.0.0` - First stable release
  - `v1.0.1` - Bug fix release

### Tag Messages

Always include descriptive messages:
- **Milestone tags:** `"SETUP-001 Complete - Project Structure Foundation"`
- **Feature tags:** `"Voice module complete - STT, TTS, wake word"`
- **Release tags:** `"v1.0.0 - First stable release"`

---

## Creating Tags

### Automated Method (Recommended)

```bash
# Create and push tag
python scripts/maintenance/create_tag.py v0.1.0 "SETUP-001 Complete - Project Structure Foundation"

# List all tags
python scripts/maintenance/create_tag.py list
```

### Manual Method

```bash
# Create annotated tag
git tag -a v0.1.0 -m "SETUP-001 Complete - Project Structure Foundation"

# Push tag to GitHub
git push origin v0.1.0

# Push all tags
git push origin --tags
```

---

## Viewing Tags

### List Tags
```bash
# List all tags
git tag -l

# List tags sorted by version
git tag -l --sort=-version:refname

# Search tags
git tag -l "v0.1*"
```

### View Tag Details
```bash
# Show tag info
git show v0.1.0

# Show tag message
git tag -l -n1 v0.1.0
```

---

## Reverting to a Tag

### Checkout Tag (Detached HEAD)
```bash
# Checkout specific tag
git checkout v0.1.0

# View files at this version
# (You'll be in detached HEAD state)
```

### Create Branch from Tag
```bash
# Create branch from tag (recommended)
git checkout -b restore-v0.1.0 v0.1.0

# Now you can make changes and commit
```

### Compare Versions
```bash
# Compare current branch with tag
git diff v0.1.0 HEAD

# Compare two tags
git diff v0.1.0 v0.2.0
```

---

## GitHub Releases

### Creating Release from Tag

1. Go to GitHub: https://github.com/AIHUBMIND/zema-ai/releases
2. Click "Create a new release"
3. Select tag: `v0.1.0`
4. Add release title: `"v0.1.0 - Project Structure Foundation"`
5. Add release notes describing what's included
6. Click "Publish release"

### Release Notes Template

```markdown
## v0.1.0 - Project Structure Foundation

### ✅ What's Included

- Complete project structure (26 directories)
- All Python packages initialized (15 __init__.py files)
- All root configuration files
- Comprehensive documentation
- SETUP-001 verification complete

### 📦 Files Created

- 58+ files created
- Complete directory structure
- Configuration templates
- Documentation system

### 🚀 Next Steps

- SETUP-002: Configuration System
- SETUP-003: Logging System
- Hardware verification
```

---

## Version Tracking

### Files Containing Version

1. **`src/main.py`** - Application version
   ```python
   __version__ = "0.1.0"
   ```

2. **`pyproject.toml`** - Package version
   ```toml
   [project]
   version = "0.1.0"
   ```

3. **Git Tags** - Version milestones
   ```bash
   git tag -l
   ```

### Updating Version

When updating version, update both files:
1. `src/main.py`: `__version__ = "0.2.0"`
2. `pyproject.toml`: `version = "0.2.0"`
3. Create tag: `git tag -a v0.2.0 -m "Description"`

---

## Backup Strategy

### Why Tags Are Important

Tags allow you to:
1. **Revert** to any milestone if something breaks
2. **Track progress** through version history
3. **Create releases** on GitHub
4. **Compare versions** to see what changed
5. **Document milestones** for future reference

### Current Backup State

- ✅ **v0.1.0** - Project structure foundation (safe point)
- ⏳ **Future tags** - Will be created as milestones complete

---

## Quick Reference

```bash
# Create tag
python scripts/maintenance/create_tag.py v0.1.0 "Description"

# List tags
python scripts/maintenance/create_tag.py list

# Revert to tag
git checkout -b restore-v0.1.0 v0.1.0

# Compare with tag
git diff v0.1.0 HEAD

# Push tag to GitHub
git push origin v0.1.0
```

---

**Last Updated:** 2025-11-03  
**Current Version:** v0.1.0  
**Status:** ✅ Project structure foundation complete

