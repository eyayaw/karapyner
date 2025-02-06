
# Karapyner

Helps you generate Karabiner-Elements configurations with a powerful **hyper key setup with sublayers**. It's a Python retouch of [@mxstbr's](https://github.com/mxstbr/karabiner/tree/main) configuration.

## Overview

Karapyner helps you create complex keyboard modifications using Karabiner-Elements on macOS. It implements:

- Hyper key (using Caps Lock) functionality
- Maps Double-tap left shift for Caps Lock
- Multiple sublayers for different actions (apps, URLs, raycast commands, window management, etc.)
- YAML-based configuration

> [!TIP]
> Watch [Max's demonstration](https://www.youtube.com/watch?v=j4b_uQX3Vu0) of the original setup, and wonder.

## Installation

1. Install [Karabiner-Elements](https://karabiner-elements.pqrs.org/)
2. Clone this repository:
```bash
git clone https://github.com/eyayaw/karapyner.git
cd karapyner
```

3. Install dependencies:
```bash
(uv) pip install pyyaml
```

## Configuration

1. Edit `config/sublayers.yaml` to define your sublayers and bindings:

```yaml
# Define sublayer activation keys
sublayer_keys:
  browse: "b"    # web shortcuts
  open: "o"      # app launcher
  window: "w"    # window management
  raycast: "r"   # raycast commands
  move: "v"      # vim-style navigation
  system: "s"    # system controls

# Browse shortcuts
browse:
  g: "https://github.com"
  m: "https://mail.google.com"
  # ...

# App shortcuts
open:
  c: "Visual Studio Code"
  t: "Terminal"
  # ...
```

2. Generate the Karabiner configuration:
```bash
python -m karapyner.config.py
```

## Usage

### Basic Controls

- **Hyper Key**: Caps Lock

N.B. This does not remap the caps lock key to `ctrl+alt+cmd+shift`, i.e., pressing the caps lock key will not trigger all those four keys at the same time.

- **Caps Lock**: Double-tap Left Shift
- **Escape**: Tap Hyper Key (Caps Lock)

### Sublayer Access

1. Hold the Hyper key (Caps Lock)
2. Press the sublayer key (e.g., 'b' for browse)
3. Press the action key (e.g., 'g' for GitHub)

### Example Combinations

- `Hyper + b, g`: Open GitHub
- `Hyper + o, t`: Open Terminal
- `Hyper + w, h`: Move window to left half
- `Hyper + v, h`: Press left arrow key
- `Hyper + s, u`: Increase volume

## Customization

1. Modify `config/sublayers.yaml` to add/change bindings
2. Add new sublayers by creating new sections in the YAML file, then modify the `Sublayer` class in [karapyner/ktypes.py](karapyner/ktypes.py) to include the new sublayer.
3. Run `config.py` to generate the new configuration


## Notes
> [!WARNING]
> **Backup your existing Karabiner configuration before using this**.
- Works on macOS with Karabiner-Elements
- Copy the generated configuration (or set the path in [config/paths.py](config/paths.py)) to `~/.config/karabiner/karabiner.json`
  ```sh
  ln karabiner.json ~/.config/karabiner/karabiner.json # add --force to overwrite
  ```

## Credit

Credit goes to [@mxstbr](https://github.com/mxstbr) for the original idea and implementation.
And, to Claude Sonnet 3.5---via GitHub Copilot in Zed---for helping translate the typescript code to Python.
