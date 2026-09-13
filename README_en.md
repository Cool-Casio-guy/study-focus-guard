# Study Focus Guard

Nếu là người dùng Tiếng Việt, hãy xem [README](./README.md)

A small Python tool that helps you stay focused while studying by checking your open windows/browser tabs, and auto-closing anything that isn't study-related during your focus session.

## How it works

1. **On start** — scans all open windows/tabs and matches them against "study material" keywords that you define yourself. You confirm or clean up before starting.
2. **While running** — any new window/tab that doesn't match your keywords gets closed (on Windows) or flagged (on macOS/Linux), along with a **"You have to focus!"** popup.
3. **Forgot to whitelist something?** — type `add` in the console to whitelist the tab/window that was just flagged.
4. **To stop** — type `stop` in the console at any time.

## Installation

```bash
pip install pygetwindow
```

## Run

```bash
python study_focus_guard.py
```

## Notes

- Auto-closing windows is fully supported on **Windows** only (a `pygetwindow` limitation). On macOS/Linux the tool will still detect and warn you, just not force-close the window.
- Browser tab detection relies on the title of the currently focused tab, not a full list of background tabs.

Created with the support of Claude
