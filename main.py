"""FocusFlow — responsive cross-platform starter application."""
from datetime import datetime
from pathlib import Path
import sqlite3

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

APP_DIR = Path.home() / ".focusflow"
APP_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = APP_DIR / "focusflow.sqlite3"

KV = r"""
<FocusRoot>:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: 0.055, 0.075, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size

    ScrollView:
        do_scroll_x: False
        bar_width: dp(5)
        GridLayout:
            id: page_content
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            padding: [dp(20) if root.width >= dp(600) else dp(12), dp(12)]
            spacing: dp(12)

            # Header
            BoxLayout:
                size_hint_y: None
                height: dp(48)
                spacing: dp(8)
                Label:
                    text: "[b]FocusFlow[/b]"
                    markup: True
                    font_size: dp(25) if root.width >= dp(420) else dp(21)
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                    color: 0.92, 0.95, 1, 1
                Label:
                    text: "" if root.width < dp(420) else "FOCUS • PLAN • GROW"
                    size_hint_x: 0.9
                    font_size: dp(10)
                    color: 0.48, 0.75, 0.92, 1
                    halign: "right"
                    valign: "middle"
                    text_size: self.size

            # Focus timer card. Its minimum height prevents controls and labels
            # from colliding in a short, restored desktop window.
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: max(dp(300), root.height * 0.40)
                padding: [dp(18) if root.width >= dp(600) else dp(12), dp(14)]
                spacing: dp(8)
                canvas.before:
                    Color:
                        rgba: 0.10, 0.13, 0.20, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(18)]

                Label:
                    text: root.mode
                    size_hint_y: None
                    height: dp(28)
                    color: 0.55, 0.78, 0.96, 1
                    font_size: dp(14)

                Label:
                    text: root.time_text
                    font_size: min(dp(56), max(dp(36), root.width * 0.085))
                    bold: True
                    color: 1, 1, 1, 1
                    halign: "center"
                    valign: "middle"
                    text_size: self.size

                Label:
                    text: "A little progress, consistently."
                    size_hint_y: None
                    height: dp(24)
                    color: 0.65, 0.70, 0.80, 1
                    font_size: dp(14)

                BoxLayout:
                    orientation: "vertical" if root.width < dp(520) else "horizontal"
                    size_hint_y: None
                    height: dp(104) if root.width < dp(520) else dp(48)
                    spacing: dp(8)
                    Button:
                        text: "Pause" if root.running else "Start"
                        size_hint_y: None
                        height: dp(48)
                        on_release: root.toggle_timer()
                        background_normal: ""
                        background_color: 0.18, 0.55, 0.78, 1
                    Button:
                        text: "Reset"
                        size_hint_y: None
                        height: dp(48)
                        on_release: root.reset_timer()
                        background_normal: ""
                        background_color: 0.22, 0.27, 0.37, 1

            # Tasks heading
            BoxLayout:
                size_hint_y: None
                height: dp(38)
                spacing: dp(8)
                Label:
                    text: "[b]Today's tasks[/b]"
                    markup: True
                    font_size: dp(18)
                    halign: "left"
                    valign: "middle"
                    text_size: self.size
                    color: 0.92, 0.95, 1, 1
                Label:
                    text: "" if root.width < dp(420) else "Saved on this device"
                    size_hint_x: 1.1
                    font_size: dp(11)
                    halign: "right"
                    valign: "middle"
                    text_size: self.size
                    color: 0.55, 0.62, 0.72, 1

            # Task entry switches to a vertical arrangement on narrow windows.
            BoxLayout:
                orientation: "vertical" if root.width < dp(520) else "horizontal"
                size_hint_y: None
                height: dp(96) if root.width < dp(520) else dp(44)
                spacing: dp(8)
                TextInput:
                    id: task_input
                    hint_text: "Add a task..."
                    multiline: False
                    padding: [dp(12), dp(10)]
                    background_color: 0.12, 0.16, 0.23, 1
                    foreground_color: 1, 1, 1, 1
                    hint_text_color: 0.55, 0.60, 0.70, 1
                    on_text_validate:
                        root.add_task(self.text)
                        self.text = ""
                Button:
                    text: "Add"
                    size_hint_x: None if root.width >= dp(520) else 1
                    width: dp(76) if root.width >= dp(520) else self.parent.width
                    size_hint_y: None
                    height: dp(44)
                    on_release:
                        root.add_task(task_input.text)
                        task_input.text = ""
                    background_normal: ""
                    background_color: 0.20, 0.48, 0.38, 1

            # Task rows grow naturally; the outer page scrolls when needed.
            GridLayout:
                id: task_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(6)

            Label:
                text: "FocusFlow starter • Offline-first • More features planned"
                size_hint_y: None
                height: dp(24)
                font_size: dp(10)
                color: 0.45, 0.52, 0.63, 1
"""

class FocusRoot(BoxLayout):
    remaining = NumericProperty(25 * 60)
    running = BooleanProperty(False)
    time_text = StringProperty("25:00")
    mode = StringProperty("FOCUS SESSION")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._event = None
        self.db = sqlite3.connect(str(DB_PATH))
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )"""
        )
        self.db.commit()
        Clock.schedule_once(lambda _dt: self.refresh_tasks(), 0)

    def toggle_timer(self):
        self.running = not self.running
        if self.running and self._event is None:
            self._event = Clock.schedule_interval(self._tick, 1)
        elif not self.running and self._event is not None:
            self._event.cancel()
            self._event = None

    def _tick(self, _dt):
        if self.remaining > 0:
            self.remaining -= 1
            self._update_time()
        else:
            self.running = False
            if self._event is not None:
                self._event.cancel()
                self._event = None
            self.mode = "SESSION COMPLETE"

    def reset_timer(self):
        self.running = False
        if self._event is not None:
            self._event.cancel()
            self._event = None
        self.remaining = 25 * 60
        self.mode = "FOCUS SESSION"
        self._update_time()

    def _update_time(self):
        mins, secs = divmod(int(self.remaining), 60)
        self.time_text = f"{mins:02d}:{secs:02d}"

    def add_task(self, title):
        title = title.strip()
        if not title:
            return
        self.db.execute(
            "INSERT INTO tasks(title, created_at) VALUES (?, ?)",
            (title, datetime.now().isoformat(timespec="seconds")),
        )
        self.db.commit()
        self.refresh_tasks()

    def refresh_tasks(self):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.checkbox import CheckBox
        from kivy.uix.label import Label
        from kivy.graphics import Color, RoundedRectangle

        if "task_list" not in self.ids:
            return
        container = self.ids.task_list
        container.clear_widgets()
        rows = self.db.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id DESC"
        ).fetchall()

        for task_id, title, completed in rows:
            row = BoxLayout(
                size_hint_y=None, height=dp(44), spacing=dp(8),
                padding=(dp(8), dp(2)),
            )
            with row.canvas.before:
                Color(0.12, 0.16, 0.23, 1)
                background = RoundedRectangle(
                    pos=row.pos, size=row.size, radius=[dp(8)]
                )
            row.bind(
                pos=lambda widget, _value, bg=background: setattr(bg, "pos", widget.pos),
                size=lambda widget, _value, bg=background: setattr(bg, "size", widget.size),
            )

            check = CheckBox(active=bool(completed), size_hint_x=None, width=dp(38))
            check.bind(
                active=lambda _widget, value, tid=task_id:
                    self.set_task_done(tid, value)
            )
            label = Label(
                text=title,
                halign="left",
                valign="middle",
                color=(0.55, 0.62, 0.72, 1) if completed else (0.92, 0.95, 1, 1),
                shorten=True,
                shorten_from="right",
            )
            label.bind(size=lambda widget, _value: setattr(widget, "text_size", widget.size))
            row.add_widget(check)
            row.add_widget(label)
            container.add_widget(row)

    def set_task_done(self, task_id, done):
        self.db.execute(
            "UPDATE tasks SET completed=? WHERE id=?",
            (int(done), task_id),
        )
        self.db.commit()
        self.refresh_tasks()


class FocusFlowApp(App):
    title = "FocusFlow"

    def build(self):
        Builder.load_string(KV)
        return FocusRoot()

    def on_stop(self):
        if self.root and hasattr(self.root, "db"):
            self.root.db.close()


if __name__ == "__main__":
    FocusFlowApp().run()
