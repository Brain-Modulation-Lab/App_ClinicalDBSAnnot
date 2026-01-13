# Clinical DBS Annotator

A professional PyQt5-based application for annotating Deep Brain Stimulation (DBS) clinical programming sessions. This tool helps clinicians systematically record stimulation parameters, clinical scales, and session observations during DBS programming.

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Multi-step Wizard Interface**: Intuitive step-by-step workflow for data collection
- **Clinical Scales Management**: Support for standard clinical assessment scales (YBOCS, MADRS, UPDRS, FTM, etc.)
- **Session Tracking**: Real-time recording of stimulation parameters and clinical observations
- **TSV Data Export**: Structured data export in tab-separated format for analysis
- **Preset Configurations**: Quick-load presets for different conditions (OCD, MDD, PD, ET)
- **Professional UI**: Dark-themed interface with increment/decrement controls for precise parameter adjustment
- **Cross-platform**: Works on Windows and macOS
- **Percept Integration**: Designed to align with Medtronic Percept data timestamps

## Project Structure

```
clinical-dbs-annotator/
├── src/
│   └── clinical_dbs_annotator/
│       ├── models/              # Data models
│       │   ├── clinical_scale.py
│       │   ├── stimulation.py
│       │   └── session_data.py
│       ├── views/               # UI views
│       │   ├── base_view.py
│       │   ├── step1_view.py
│       │   ├── step2_view.py
│       │   ├── step3_view.py
│       │   └── wizard_window.py
│       ├── controllers/         # Business logic
│       │   └── wizard_controller.py
│       ├── ui/                  # UI components
│       │   └── widgets.py
│       ├── utils/               # Utilities
│       │   ├── graphics.py
│       │   └── resources.py
│       ├── config.py            # Configuration
│       ├── __init__.py
│       └── __main__.py          # Entry point
├── tests/                       # Test suite
│   ├── unit/
│   └── ui/
├── scripts/                     # Build scripts
│   ├── build_windows.py
│   ├── build_macos.py
│   └── create_installer.nsi
├── icons/                       # Application icons
├── style.qss                    # Qt stylesheet
├── pyproject.toml              # Project configuration
└── README.md
```

## Installation

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

```bash
# Install uv if not already installed
pip install uv

# Clone the repository
git clone https://github.com/bml/clinical-dbs-annotator.git
cd clinical-dbs-annotator

# Install dependencies
uv pip install -e .

# For development (includes testing tools)
uv pip install -e ".[dev]"

# For building executables
uv pip install -e ".[build]"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/bml/clinical-dbs-annotator.git
cd clinical-dbs-annotator

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

## Usage

### Running from Source

```bash
# Using the installed command
clinical-dbs-annotator

# Or using Python module
python -m clinical_dbs_annotator
```

### Workflow

1. **Step 1: Initial Settings**
   - Select TSV output file location
   - Configure initial stimulation parameters
   - Enter baseline clinical scale values
   - Add initial notes

2. **Step 2: Session Scales**
   - Select scales to track during the session (e.g., Mood, Anxiety, Energy)
   - Configure scale ranges

3. **Step 3: Active Session**
   - Adjust stimulation parameters in real-time
   - Record scale values at different timepoints
   - Add session notes
   - Insert rows to save observations
   - Close session when complete

### Clinical Presets

The application includes presets for common conditions:

- **OCD**: YBOCS, YBOCS-o, YBOCS-c, MADRS
- **MDD**: MADRS
- **PD**: UPDRS, PDQ
- **ET**: FTM

Session scale presets:
- **OCD/MDD**: Mood, Anxiety, Energy, OCD/Rumination
- **PD/ET**: Tremor, Rigidity

## Development

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=clinical_dbs_annotator --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py
```

### Code Quality

```bash
# Format code with black
black src/

# Lint with ruff
ruff check src/

# Type checking with mypy
mypy src/
```

## Building Executables

### Windows

```bash
# Install build dependencies
uv pip install -e ".[build]"

# Build executable
python scripts/build_windows.py

# The executable will be in dist/ folder
```

#### Creating Windows Installer

1. Install [NSIS](https://nsis.sourceforge.io/)
2. Build the executable first
3. Right-click on `scripts/create_installer.nsi` and select "Compile NSIS Script"
4. The installer will be created in `dist/` folder

### macOS

```bash
# Install build dependencies
uv pip install -e ".[build]"

# Build application
python scripts/build_macos.py

# The .app bundle will be in dist/ folder
```

## Data Format

The application exports data in TSV (Tab-Separated Values) format with the following columns:

- `date`: Recording date (YYYY-MM-DD)
- `time`: Recording time (HH:MM:SS in Eastern Time)
- `block_id`: Sequential block identifier
- `scale_name`: Name of the clinical/session scale
- `scale_value`: Value of the scale
- `stim_freq`: Stimulation frequency (Hz)
- `left_contact`: Left electrode contact
- `left_amplitude`: Left stimulation amplitude (mA)
- `left_pulse_width`: Left pulse width (µs)
- `right_contact`: Right electrode contact
- `right_amplitude`: Right stimulation amplitude (mA)
- `right_pulse_width`: Right pulse width (µs)
- `notes`: Additional notes

## Architecture

The application follows the **Model-View-Controller (MVC)** pattern:

- **Models** (`models/`): Data structures and business logic for clinical data
- **Views** (`views/`): PyQt5 UI components and layouts
- **Controllers** (`controllers/`): Coordination between models and views
- **Config** (`config.py`): Centralized configuration and constants
- **Utils** (`utils/`): Helper functions for graphics and resources

### Key Design Patterns

- **Dataclasses**: Used for model definitions (Python 3.7+)
- **Context Manager**: SessionData supports `with` statement for automatic file handling
- **Observer Pattern**: PyQt signals/slots for UI event handling
- **Factory Pattern**: View creation and initialization
- **Strategy Pattern**: Different presets for different clinical conditions

## Dependencies

### Core Dependencies
- PyQt5 5.15.10 - GUI framework
- pytz >= 2025.2 - Timezone support

### Development Dependencies
- pytest >= 8.0.0 - Testing framework
- pytest-qt >= 4.4.0 - PyQt5 testing support
- pytest-cov >= 4.1.0 - Coverage reporting
- black >= 24.0.0 - Code formatter
- ruff >= 0.1.0 - Linter
- mypy >= 1.8.0 - Type checker

### Build Dependencies
- pyinstaller >= 6.15.0 - Executable bundler
- opencv-python-headless >= 4.12.0.88 - Image processing

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Format code (`black src/`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **BML** - Initial work

## Acknowledgments

- Built for clinical DBS programming session annotation
- Designed for use with Medtronic Percept systems
- Follows clinical best practices for data recording

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Changelog

### Version 0.1.0 (Initial Release)
- Multi-step wizard interface
- Clinical and session scale management
- Real-time parameter adjustment
- TSV data export
- Windows and macOS support
- Comprehensive test suite
- Professional deployment scripts
