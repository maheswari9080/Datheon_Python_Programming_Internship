# Task 03: Automated File Organizer & Cleanup Utility

Part of the **Datheon Python Internship Project Suite**.

## Overview
A robust, safe filesystem automation utility written in Python using `pathlib`, `shutil`, and `os.scandir()`. It organizes clutter in user-selected directories (e.g. Downloads or desktop drops) by grouping files into clean semantic categories based on file extension.

---

## Supported Categories & Taxonomy
- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`
- **Videos**: `.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`
- **Audio**: `.mp3`, `.wav`, `.aac`, `.flac`, `.m4a`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`
- **Code**: `.py`, `.js`, `.ts`, `.html`, `.css`, `.java`, `.c`, `.cpp`, `.json`, `.xml`
- **Spreadsheets**: `.csv`, `.xls`, `.xlsx`, `.ods`
- **Presentations**: `.ppt`, `.pptx`, `.odp`
- **Other**: Unrecognized or extensionless files

---

## Safety Features
1. **Protected Path Validator**: Strictly refuses to organize root filesystems (`C:\`, `/`), system folders (`System32`, `Program Files`, `/bin`), or the project repository directory itself.
2. **Dry-Run Simulation**: `--dry-run` simulates the entire run and outputs a preview of moves without altering any file.
3. **Collision Handling**:
   - `rename` (Default): Appends increments like `filename_1.ext` to protect existing files.
   - `skip`: Leaves conflicting source files untouched.
   - `overwrite`: Overwrites destination only when explicitly requested.
4. **Recursion Prevention**: Skips directories and existing category folders so re-running the utility never duplicates or nests folders.
5. **Detailed Audit Logging**: Every scan, move, collision, and error is recorded with timestamps in `logs/organizer_audit.log`.

---

## How to Run

### Recommended: Dry-Run Preview First
```bash
python task3_file_organizer/organizer.py --target "C:\Users\YourName\Downloads" --dry-run
```

### Live Organization with Confirmation Prompt
```bash
python task3_file_organizer/organizer.py --target "C:\Users\YourName\Downloads"
```

### Non-Interactive Automation with Skip Collision Policy
```bash
python task3_file_organizer/organizer.py --target "C:\Users\YourName\Downloads" --collision skip --non-interactive
```

---

## Exit Codes
- `0`: Success (all files categorized cleanly)
- `1`: Partial failure (one or more individual file permission errors logged)
- `2`: Fatal error (unsafe target directory, invalid argument, or missing folder)

---

## Automated Testing
Run the 12 unit tests using temporary sandboxes:
```bash
python -m unittest discover -s task3_file_organizer/tests -p "test_*.py" -v
```
No live user folders or real system files are ever modified during testing.
