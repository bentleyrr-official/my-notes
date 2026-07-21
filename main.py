import os
import sys
import webview

CODE_EXTENSIONS = {
    ".py": "python", ".js": "javascript", ".ts": "typescript", ".jsx": "javascript",
    ".tsx": "typescript", ".java": "java", ".c": "c", ".cpp": "cpp", ".h": "c",
    ".hpp": "cpp", ".cs": "csharp", ".go": "go", ".rb": "ruby", ".php": "php",
    ".html": "html", ".htm": "html", ".css": "css", ".json": "json", ".xml": "xml",
    ".sh": "bash", ".sql": "sql", ".rs": "rust", ".swift": "swift", ".kt": "kotlin",
    ".md": "markdown", ".yaml": "yaml", ".yml": "yaml",
}


def detect_language(path):
    ext = os.path.splitext(path)[1].lower()
    return CODE_EXTENSIONS.get(ext, "plain")


def base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_html():
    html_path = os.path.join(base_dir(), "notes_ui.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


class Api:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window

    def open_file(self):
        result = self.window.create_file_dialog(
            webview.FileDialog.OPEN,
            file_types=("All files (*.*)",),
        )
        if not result:
            return None
        path = result[0]
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="latin-1") as f:
                content = f.read()
        except OSError as e:
            return {"error": str(e)}
        return {
            "path": path,
            "name": os.path.basename(path),
            "content": content,
            "language": detect_language(path),
        }

    def save_file(self, path, content):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"ok": True}
        except OSError as e:
            return {"ok": False, "error": str(e)}

    def save_file_as(self, content):
        path = self.window.create_file_dialog(
            webview.FileDialog.SAVE,
            save_filename="Untitled.txt",
        )
        if not path:
            return None
        if isinstance(path, (list, tuple)):
            path = path[0]
        result = self.save_file(path, content)
        if not result.get("ok"):
            return {"error": result.get("error", "Could not save file")}
        return {
            "path": path,
            "name": os.path.basename(path),
            "language": detect_language(path),
        }

    def confirm_discard(self, message):
        return self.window.create_confirmation_dialog("My Notes", message)


def main():
    if sys.platform == "win32":
        os.environ.setdefault(
            "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS",
            "--force-renderer-accessibility=off",
        )
    api = Api()
    window = webview.create_window(
        "Untitled - My Notes",
        html=load_html(),
        js_api=api,
        width=1000,
        height=700,
        min_size=(640, 420),
        text_select=True,
        background_color="#ffffff",
    )
    api.set_window(window)
    icon_path = os.path.join(base_dir(), "My Notes.ico")
    kwargs = {}
    if os.path.exists(icon_path):
        kwargs["icon"] = icon_path
    webview.start(**kwargs)


if __name__ == "__main__":
    main()