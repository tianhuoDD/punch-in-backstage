# utils/logger.py
from flask import current_app

class LazyLogger:
    def __getattr__(self, name):
        return getattr(current_app.logger, name)

logger = LazyLogger()