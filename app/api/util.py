class DebugPrint:
    level = 0

    def __init__(self, level: int = 0):
        DebugPrint.level = level

    def set_level(self, level: int):
        DebugPrint.level = level

    def get_level(self):
        return DebugPrint.level

    def debug_print(self, msg, debug_level: int = 3):
        if 0 < debug_level <= self.get_level():
            print("DEBUG(", debug_level, "): " + msg, sep="")
