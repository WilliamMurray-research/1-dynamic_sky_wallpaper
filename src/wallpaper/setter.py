import platform
import subprocess
import ctypes
from pathlib import Path


def set_wallpaper(path: Path):
    """
    Cross‑platform deterministic wallpaper setter.
    Accepts a Path to a PNG file.
    """

    system = platform.system().lower()

    if system == "darwin":
        _set_macos(path)
    elif system == "windows":
        _set_windows(path)
    elif system == "linux":
        _set_linux(path)
    else:
        print(f"Unsupported OS: {system}")


# ------------------------------------------------------------
# macOS
# ------------------------------------------------------------

def _set_macos(path: Path):
    """
    Uses AppleScript to set wallpaper on macOS.
    Deterministic and stable.
    """

    script = f'''
    tell application "System Events"
        set picture of every desktop to "{path}"
    end tell
    '''

    subprocess.run(["osascript", "-e", script], check=False)


# ------------------------------------------------------------
# Windows
# ------------------------------------------------------------

def _set_windows(path: Path):
    """
    Uses SystemParametersInfoW via ctypes.
    Deterministic and stable.
    """

    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02

    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        str(path),
        SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    )


# ------------------------------------------------------------
# Linux (GNOME / KDE)
# ------------------------------------------------------------

def _set_linux(path: Path):
    """
    Supports GNOME and KDE Plasma.
    Falls back silently if unsupported.
    """

    # GNOME
    try:
        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.background",
            "picture-uri",
            f"file://{path}"
        ], check=False)
        return
    except Exception:
        pass

    # KDE Plasma
    try:
        script = f"""
        var Desktops = desktops();
        for (i=0;i<Desktops.length;i++) {{
            d = Desktops[i];
            d.wallpaperPlugin = "org.kde.image";
            d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
            d.writeConfig("Image", "file://{path}");
        }}
        """
        subprocess.run(["qdbus-qt5", "org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", script], check=False)
        return
    except Exception:
        pass

    print("Linux wallpaper setter: no supported desktop environment detected.")
