from pathlib import Path


__all__ = [
    "__version__",
    "__static_folder__",
    "__static_src_folder__",
]

__version__ = "0.0.1"
__static_folder__ = Path(__file__).parent / "static"
__static_src_folder__ = __static_folder__ / "tailwindcss" / "src"
