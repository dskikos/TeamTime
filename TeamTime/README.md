# TeamTime - Productivity Tracker

A Python-based productivity tracker that monitors laptop activity, categorizes usage, and gamifies study goals with a dynamic progress bar system.

## Features

- **Activity Monitoring**: Tracks active window/application names and durations
- **Smart Categorization**: Categorizes activities as Productive, Neutral, or Distracting
- **Goal Setting**: Set daily study time goals with real-time progress tracking
- **Progress Bar**: Visual progress bar with penalty system for distractions
- **Dashboard**: Real-time statistics and activity display
- **Local Storage**: All data stored locally in SQLite database

## Installation

### 1. Create Virtual Environment

```bash
cd TeamTime
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
cd src
python main.py
```

## Usage

1. **Set a Goal**: Click "Set Goal" and enter your daily productivity target in minutes
2. **Start Tracking**: Click "Start Tracking" to begin monitoring your activity
3. **Monitor Progress**: Watch your progress bar update in real-time
4. **Stop Tracking**: Click "Stop Tracking" when done

## Progress Calculation

- **Productive time** adds to your progress
- **Distracting time** subtracts from progress (50% penalty by default)
- **Neutral time** is tracked but doesn't affect progress
- Progress percentage = (Effective Minutes / Target Minutes) × 100

## Customization

### Adding Custom Categories

Edit `config/categories.json` to add or remove applications from categories:

```json
{
  "productive": ["vscode", "pycharm", "notion"],
  "distracting": ["instagram", "youtube", "netflix"],
  "neutral": ["spotify", "slack", "email"]
}
```

## Project Structure

```
TeamTime/
├── src/
│   ├── monitor/           # Activity tracking modules
│   ├── database/          # Database models and manager
│   ├── ui/                # PyQt5 dashboard interface
│   ├── core/              # Goal and progress logic
│   └── main.py            # Entry point
├── data/                  # SQLite database (auto-generated)
├── config/                # Configuration files
├── requirements.txt       # Python dependencies
└── README.md
```

## Platform Support

- **Windows**: Full support (uses pygetwindow)
- **macOS**: Requires AppKit (install with: `pip install pyobjc-framework-Cocoa`)
- **Linux**: Requires xdotool (install with: `sudo apt-get install xdotool`)

## Troubleshooting

### Windows: Module not found errors
Make sure you're in the `src` directory when running the application:
```bash
cd src
python main.py
```

### Permission Errors
On some systems, you may need to grant accessibility permissions for window tracking.

## License

MIT License - Feel free to use and modify for your hackathon!
