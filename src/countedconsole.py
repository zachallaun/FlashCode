import code

class CountedConsole(code.InteractiveConsole):
    """
    Used in the exact same way as code.InteractiveConsole.
    The self.raw_input() method has been redefined to stylize the prompt
    and count lines.
    """
    
    def __init__(self):
        code.InteractiveConsole.__init__(self)
        self.linecount = 0
    
    def raw_input(self, prompt=''):
        self.linecount += 1

        # Prompt color: green if ">>>", yellow if "..."
        color = "\033[92m" if ">" in prompt else "\033[93m"
        pre = "{0}({1})\033[0m".format(color, str(self.linecount))

        return input(pre + prompt)
