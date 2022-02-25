class Console:
    ANSI_OK = "\033[92m"  # GREEN
    ANSI_WARN = "\033[93m"  # YELLOW
    ANSI_ERROR = "\033[91m"  # RED
    ANSI_RESET = "\033[0m"  # RESET COLOR

    @classmethod
    def plain(cls, message):
        print(message)

    @classmethod
    def ok(cls, message):
        print(f"{cls.ANSI_OK}{message}{cls.ANSI_RESET}")

    @classmethod
    def warn(cls, message):
        print(f"{cls.ANSI_WARN}{message}{cls.ANSI_RESET}")

    @classmethod
    def error(cls, message):
        print(f"{cls.ANSI_ERROR}{message}{cls.ANSI_RESET}")
