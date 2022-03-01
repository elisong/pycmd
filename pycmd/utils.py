import re


class Console:
    ANSI_INFO = "\033[92m"  # GREEN
    ANSI_WARN = "\033[93m"  # YELLOW
    ANSI_ERROR = "\033[91m"  # RED
    ANSI_RESET = "\033[0m"  # RESET
    ANSI_BOLD = "\u001b[1m"  # BOLD
    ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    @classmethod
    def plain(cls, message):
        print(f"{'':2}{message}")

    @classmethod
    def info(cls, message):
        print(f"{cls.ANSI_INFO}✓ {message}{cls.ANSI_RESET}")

    @classmethod
    def warn(cls, message):
        print(f"{cls.ANSI_WARN}! {message}{cls.ANSI_RESET}")

    @classmethod
    def error(cls, message):
        print(f"{cls.ANSI_ERROR}✗ {message}{cls.ANSI_RESET}")

    @classmethod
    def escape(cls, message):
        return cls.ANSI_ESCAPE.sub("", message.decode("utf-8").strip())
