class Logger:
    def __init__(self):
        pass
    
    def _print(self, level, message):
        print(f'[{level}] {message}')
    
    def debug(self, message):
        self._print('DEBUG', message)
    
    def info(self, message):
        self._print('INFO', message)
    
    def warning(self, message):
        self._print('WARNING', message)
    
    def error(self, message):
        self._print('ERROR', message)

def get_logger():
    """
    Get a simple logger instance that prints to console with level prefix.

    Returns:
        Logger instance
    """
    return Logger()

