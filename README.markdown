# FlashCode
### Interactive Python Tutorial

#### Usage
    $ python3.2 run.py

#### Extensibility
Modules live in `data/`, and are declared in `data/manifest.txt`. Format your manifest module declarations as seen in the file. Manifest supports full-line comments with `#`.

Format modules as seen in `data/begtut.txt`. Regular expressions for input and output are required. If you simply want a catch-all, use `r".*"`. Currently, validation will only occur on some kind of output. (This is why the variables module requires declared variables to be printed.)

#### The MIT License
Copyright (c) 2011 Zachary Allaun

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.