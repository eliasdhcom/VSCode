![logo](https://eliasdh.com/assets/media/images/logo-github.png)
# 💙🤍README🤍💙

## 📘Table of Contents

1. [📘Table of Contents](#📘table-of-contents)
2. [🖖Introduction](#🖖introduction)
3. [🎨Colors](#🎨colors)
4. [🚀How to use](#🚀how-to-use)
5. [🛠️Development](#🛠️development)
6. [🔗Links](#🔗links)

---

## 🖖Introduction

The official EliasDH theme for Visual Studio Code. It ships an **EliasDH Dark** and an **EliasDH Light** variant, built on the same design tokens as [EliasDH.com](https://eliasdh.com), [app.eliasdh.com](https://app.eliasdh.com) and DHMail, so your editor looks like the rest of the EliasDH platform.

Please also see following documents:
- [LICENSE](LICENSE.md)
- [SECURITY](SECURITY.md)
- [CONTRIBUTING](CONTRIBUTING.md)
- [CODE OF CONDUCT](CODE-OF-CONDUCT.md)

## 🎨Colors

| Token             | Dark      | Light     |
|-------------------|-----------|-----------|
| Editor background | `#060709` | `#ffffff` |
| Surface           | `#0d1016` | `#f6f7f9` |
| Primary           | `#0f54ae` | `#4f94f0` |
| Ink (accent text) | `#86b6ff` | `#4077bf` |
| Text              | `#edeff2` | `#0c0e11` |
| Secondary         | `#818a92` | `#6c757d` |
| Success           | `#199e70` | `#1baf7a` |
| Danger            | `#f87171` | `#e74c3c` |

## 🚀How to use

### Option 1: Install from VSIX (recommended)

1. Download the latest `.vsix` file from the [Release](Release) folder (open the file and click **Download raw file**).
2. Install it:
    - **In VS Code:** open the Extensions view (`Ctrl+Shift+X`), click the `...` menu at the top right, choose **Install from VSIX...** and select the downloaded file.
    - **Or from a terminal:**
        ```bash
        code --install-extension eliasdh-theme-1.0.0.vsix
        ```
3. Press `Ctrl+K` then `Ctrl+T` (macOS: `Cmd+K` then `Cmd+T`) and pick **EliasDH Dark** or **EliasDH Light**.

### Option 2: Clone into your extensions folder

```bash
# Windows (PowerShell)
git clone https://github.com/eliasdhcom/VSCode.git "$env:USERPROFILE\.vscode\extensions\eliasdh-theme"

# macOS / Linux
git clone https://github.com/eliasdhcom/VSCode.git ~/.vscode/extensions/eliasdh-theme
```

Restart VS Code and select the theme with `Ctrl+K` `Ctrl+T`. Run `git pull` in that folder to update.

### Follow your OS light/dark mode (optional)

Add this to your `settings.json` to switch automatically:

```json
{
    "window.autoDetectColorScheme": true,
    "workbench.preferredDarkColorTheme": "EliasDH Dark",
    "workbench.preferredLightColorTheme": "EliasDH Light"
}
```

## 🛠️Development

The theme files in [themes](themes) are generated from the design tokens in [scripts/build.py](scripts/build.py). To change a color:

1. Edit the palette in `scripts/build.py`.
2. Bump `version` in [package.json](package.json).
3. Run `python scripts/build.py`. This regenerates the themes and writes a new `.vsix` to [Release](Release).

## 🔗Links
- 👯 Web hosting company [EliasDH.com](https://eliasdh.com).
- 📫 How to reach us info@eliasdh.com
