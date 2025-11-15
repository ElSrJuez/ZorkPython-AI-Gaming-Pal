from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
import time

class RichZorkUI:
    def __init__(self):
        self.console = Console()
        # Layout: top body (split 40/60) + 2-line bottom prompt bar
        self.layout = Layout()
        # Body + prompt bar (fixed 3 rows incl. borders ≈ 2 text lines)
        self.layout.split_column(
            Layout(name="body", ratio=1),
            Layout(name="prompt", size=4),
        )
        # Inside body create left/right columns 40 / 60
        self.layout["body"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=3),
        )
        self.zork_lines = []
        self.ai_lines = []
        self.prompt_text = ""
        self._get_scroll_height()

    def _get_scroll_height(self):
        # rough panel height ≈ terminal height minus borders and prompt bar
        # two text lines + panel borders (~2) = 4 rows reserved
        self.scroll_h = max(1, self.console.size.height - 8)

    def render(self):
        left = "\n".join(self.zork_lines[-self.scroll_h :])
        right = "\n".join(self.ai_lines[-self.scroll_h :])
        self.layout["left"].update(Panel(left, title="Zork Output", border_style="green"))
        self.layout["right"].update(Panel(right, title="AI Output", border_style="cyan"))
        # prompt bar content
        self.layout["prompt"].update(Panel(self.prompt_text, title="Prompt", border_style="magenta"))
        return self.layout

    def start(self):
        self.live = Live(self.render(), console=self.console, refresh_per_second=10)
        self.live.start()

    def set_prompt(self, text: str):
        """Update the bottom prompt bar text."""
        self.prompt_text = text
        # Ensure prompt shows immediately if live started
        if hasattr(self, "live"):
            self.live.update(self.render())

    def stop(self):
        self.live.stop()

    def append_zork(self, text: str):
        self.zork_lines.append(text)
        self.live.update(self.render())

    def append_ai(self, text: str):
        self.ai_lines.append(text)
        self.live.update(self.render())

if __name__ == "__main__":
    ui = RichZorkUI()
    ui.start()
    # demo
    for i in range(30):
        ui.append_zork(f"Room description line {i}")
        ui.append_ai(f"AI says: response {i}")
        time.sleep(0.2)
    time.sleep(2)
    ui.stop()