import logging
import re


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    BOLD = "\033[1m"
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        # **text** to bold
        record.msg = re.sub(r"\*\*(.*?)\*\*", rf"{self.BOLD}\1{self.RESET}", record.msg)
        return super().format(record)


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter("%(levelname)s:     %(message)s"))
    logger.addHandler(handler)

    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("amqtt").setLevel(logging.WARNING)
    logging.getLogger("mqtt").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
