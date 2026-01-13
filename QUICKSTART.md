# Quick Start Guide

This guide will help you get the Clinical DBS Annotator up and running quickly.

## Prerequisites

- Python 3.11 or higher
- Windows or macOS
- uv package manager (recommended) or pip

## Installation (5 minutes)

### Option 1: Using uv (Recommended - Fastest)

```bash
# 1. Install uv if needed
pip install uv

# 2. Navigate to project directory
cd App_ClinicalDBSAnnot

# 3. Install the application
uv pip install -e .
```

### Option 2: Using pip

```bash
# 1. Navigate to project directory
cd App_ClinicalDBSAnnot

# 2. Install the application
pip install -e .
```

## Running the Application

```bash
# Run from anywhere after installation
python -m clinical_dbs_annotator

# Or use the command
clinical-dbs-annotator
```

## First Use

### Step 1: Initial Setup (2 minutes)
1. Click "Browse" to select where to save your data file (*.tsv)
2. Enter initial stimulation parameters:
   - Frequency (Hz)
   - Left and right contact, amplitude (mA), pulse width (µs)
3. Click a preset button (OCD/MDD/PD/ET) or manually add clinical scales
4. Add any initial notes
5. Click "Next"

### Step 2: Session Scales (1 minute)
1. Click a preset button or add custom session scales
2. Set min/max ranges for each scale
3. Click "Next"

### Step 3: Recording Session
1. Adjust stimulation parameters as needed using +/- buttons
2. Enter current scale values
3. Add session notes
4. Click "Insert" to record the current state (timestamps automatically)
5. Repeat steps 1-4 as you adjust parameters
6. Click "Close session" when done

## Example Workflow for OCD Patient

```
Step 1:
- File: patient001_session1.tsv
- Frequency: 130 Hz
- Contacts: e1 (left), e2 (right)
- Amplitudes: 3.5 mA (left), 4.0 mA (right)
- Pulse widths: 60 µs (both)
- Click "OCD" preset → Auto-fills YBOCS, YBOCS-o, YBOCS-c, MADRS
- Enter baseline scores
- Click "Next"

Step 2:
- Click "OCD" preset → Auto-fills Mood, Anxiety, Energy, OCD scales
- Click "Next"

Step 3:
- Enter initial scale values (e.g., Mood: 5, Anxiety: 7)
- Click "Insert" to record baseline
- Adjust left amplitude to 4.0 mA
- Enter new scale values
- Click "Insert" to record new state
- Continue adjusting and recording
- Click "Close session" when done
```

## Output Data

Your data is saved in TSV format with columns:
- date, time, block_id
- scale_name, scale_value
- stimulation parameters (frequency, contacts, amplitudes, pulse widths)
- notes

Import into Excel, MATLAB, Python pandas, or any analysis software.

## Tips

- Use preset buttons to quickly configure common setups
- The +/++ buttons adjust values by large/small increments
- Time is automatically recorded in Eastern Time
- Each "Insert" creates a new timestamped entry
- You can go "Back" to revise earlier steps before recording

## Troubleshooting

**Application won't start:**
```bash
# Verify installation
python -m clinical_dbs_annotator

# Check Python version
python --version  # Should be 3.11+

# Reinstall if needed
pip install -e . --force-reinstall
```

**Missing pytz error:**
```bash
pip install pytz
```

**Qt plugin error:**
```bash
pip install --upgrade pyqt5
```

## Building Standalone Executable

For users without Python installed:

```bash
# Install build tools
uv pip install -e ".[build]"

# Windows
python scripts/build_windows.py

# macOS
python scripts/build_macos.py
```

The executable will be in the `dist/` folder and can be distributed to others.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the [tests/](tests/) folder for usage examples
- Review [config.py](src/clinical_dbs_annotator/config.py) to customize presets
- Build a standalone executable for deployment

## Support

For issues: Check README.md or create a GitHub issue
