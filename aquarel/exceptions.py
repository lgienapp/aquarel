"""
Custom exception classes for Aquarel.
"""

class AquarelError(Exception):
    """Base exception class for all Aquarel-related errors."""
    pass


class ThemeNotFoundError(AquarelError):
    """Raised when a theme cannot be found."""
    
    def __init__(self, theme_name: str, available_themes: list):
        self.theme_name = theme_name
        self.available_themes = available_themes
        super().__init__(
            f"Theme '{theme_name}' not found. Available themes: {', '.join(available_themes)}"
        )


class ThemeValidationError(AquarelError):
    """Raised when theme data is invalid."""
    
    def __init__(self, field: str, value: str, valid_values: list = None):
        self.field = field
        self.value = value
        self.valid_values = valid_values
        
        if valid_values:
            super().__init__(
                f"Invalid value '{value}' for field '{field}'. "
                f"Valid values: {', '.join(map(str, valid_values))}"
            )
        else:
            super().__init__(f"Invalid value '{value}' for field '{field}'")


class ThemeLoadError(AquarelError):
    """Raised when theme loading fails."""
    
    def __init__(self, filename: str, reason: str):
        self.filename = filename
        self.reason = reason
        super().__init__(f"Failed to load theme from '{filename}': {reason}")


class TransformError(AquarelError):
    """Raised when transform application fails."""
    
    def __init__(self, transform_name: str, reason: str):
        self.transform_name = transform_name
        self.reason = reason
        super().__init__(f"Transform '{transform_name}' failed: {reason}")