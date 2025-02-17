import time
from dataclasses import dataclass

from .utils._dop import getframe

from .typings.FormatRemovalError import FormatRemovalError

__all__ = ("Logger", )

@dataclass
class LoggerLevel:
    level: str
    wight: int
    debug: bool = False

class Logger():
    _config = {
        "message_format": { "*": "[{time}:{level}] ({name}:{func}:{line}): {message}" },
        "print_wight": -1,
        "out_put_print": None,
        "out_put_print_text": None # edit for decoder
    }

    def __init__(self, name: str, out_print: str = None, output_text = None) -> None:
        self.name = name
        if out_print is not None:
            Logger.set_outprint(out_print)

        # edit for decoder
        if output_text is not None:
            Logger.set_outprint_text(output_text)
            
        
        
    @classmethod
    def set_format(cls, format: str, _from: str="*"):
        cls._config["message_format"][_from] = format
        
    @classmethod
    def remove_format(cls, _from: str):
        if _from == "*":
            raise FormatRemovalError("Cannot remove the format '*' because it is reserved or protected.")
        try:
            cls._config["message_format"].remove(_from)
        except ValueError:
            raise FormatRemovalError(f"The format '{_from}' does not exist in the configuration.")

    @classmethod
    def set_wight(cls, wight: int):
        cls._config["print_wight"] = wight
    
    @classmethod
    def set_outprint(cls, path: str):
        cls._config["out_put_print"] = path

    # edit for decoder
    @classmethod
    def set_outprint_text(cls, func):
        cls._config["out_put_print_text"] = func



    def _getformat(self, messages: str, level: str, format_from: str) -> str:
        _, func, line = getframe(0)
        return format_from.replace("{time}", time.strftime("%H:%M:%S", time.gmtime(time.time()))) \
                    .replace("{name}", self.name) \
                    .replace("{message}", "".join([str(message) for message in messages])) \
                    .replace("{level}", level) \
                    .replace("{func}", func) \
                    .replace("{line}", str(line)) 

    def _log(self, message: str, options: LoggerLevel, **kwargs):
        config = Logger._config["message_format"]
        send_message = self._getformat(message, options.level, \
                                        config[options.level] if options.level in config else config['*']
                                        )
        if Logger._config['print_wight'] < options.wight:
            print( send_message )
            # edit for decoder
            if Logger._config["out_put_print_text"] is not None:
                Logger._config["out_put_print_text"](send_message)

        if Logger._config['out_put_print'] is not None:
            with open(Logger._config['out_put_print'],  "a", encoding="utf-8") as logger:
                logger.write( send_message + "\n" )

        if options.debug:
            return send_message

    def debug(self, *message: str) -> None:
        self._log( message, LoggerLevel("DEBUG", 0) )

    def info(self, *message: str) -> None:
        self._log( message, LoggerLevel("INFO", 1) )

    def warm(self, *message: str) -> None:
        self._log( message, LoggerLevel("WARNUNG", 2) )

    def error(self, *message: str) -> None:
        self._log( message, LoggerLevel("ERROR", 3) )

    @classmethod
    def reset(cls):
        # edit for decoder
        cls._config = { "message_format": { "*": "[{time}:{level}] ({name}:{func}:{line}): {message}" }, "print_wight": -1, "out_put_print": None, "out_put_print_text": None }