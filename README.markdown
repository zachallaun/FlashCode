# FlashCode
### Interactive Python Tutorial

#### Usage
    python3.2 start.py

#### Extensibility
Modules live in `data/`, and are declared in `data/manifest.txt`. Format your manifest module declarations as seen in the file. Manifest supports full-line comments with `#`.

Format modules as seen in `data/begtut.txt`. Regular expressions for input and output are required. If you simply want a catch-all, use `r"\.*"`. Currently, validation will only occur on some kind of output. This is why the variables module requires declared variables to be printed.