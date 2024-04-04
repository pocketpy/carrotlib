from datetime import datetime
import sys

def _now() -> str:
    return str(datetime.now())

def _colorize(msg: str, fg: int = None, bg: int = None) -> str:
    return msg
    if fg is None and bg is None:
        return msg
    elif fg is None:
        return f'\x1b[{bg}m{msg}\x1b[0m'
    elif bg is None:
        return f'\x1b[{fg}m{msg}\x1b[0m'
    else:
        return f'\x1b[{fg};{bg}m{msg}\x1b[0m'

def _log(level: str, *args, fg=None, bg=None):
    msg = ' '.join(map(str, args))
    if sys.platform == 'android':
        print(msg)
        return
    level = level.ljust(8)
    prefix = _colorize(_now(), fg=90) + ' | ' + _colorize(level, fg=fg, bg=bg) + ' | '
    print(prefix + _colorize(msg, fg=fg, bg=bg))

def debug(*args):
    _log('DEBUG', *args, fg=94)

def info(*args):
    _log('INFO', *args)

def warning(*args):
    _log('WARNING', *args, fg=93)

def error(*args):
    _log('ERROR', *args, fg=91)

def critical(*args):
    _log('CRITICAL', *args, bg=101)