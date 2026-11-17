# Streamlit Task Manager

> A task manager with priorities, deadlines and statistics, built with Streamlit on a small domain model.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)


## Features

- Add, list and complete tasks.
- Priorities (high, medium, low) with colour markers.
- Deadlines with an overdue count.
- Statistics dashboard.
- State persists during a session.

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Model | Python dataclasses |
| Data | pandas |

## Quick Start

```bash
git clone https://github.com/dastonbek8747/streamlit-task-manager.git
cd streamlit-task-manager
python -m venv .venv && source .venv/bin/activate
pip install streamlit pandas
streamlit run app.py
```

## Project Structure

```
app.py     # Streamlit UI
main.py    # TaskManager, Task and Priority model
```

## License

MIT © 2026 Doston Sultonov.
