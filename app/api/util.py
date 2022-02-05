class DebugPrint:
    level = 0

    def __init__(self, level: int = 0):
        DebugPrint.level = level

    def set_level(self, level: int):
        DebugPrint.level = level

    def get_level(self):
        return DebugPrint.level

    def debug_print(self, debug_level: int, msg):
        if debug_level <= self.get_level():
            print("DEBUG: " + msg)
