"""FocusFlow — independent cross-platform starter application."""
from datetime import datetime
from pathlib import Path
import sqlite3

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

APP_DIR = Path.home() / ".focusflow"
APP_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = APP_DIR / "focusflow.sqlite3"

KV = r"""
<FocusRoot>:
    orientation: "vertical"
    padding: "20dp"
    spacing: "14dp"
    canvas.before:
        Color:
            rgba: 0.055, 0.075, 0.12, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        Label:
            text: "[b]FocusFlow[/b]"
            markup: True
            font_size: "25sp"
            halign: "left"
            color: 0.92, 0.95, 1, 1
        Label:
            text: "FOCUS • PLAN • GROW"
            font_size: "10sp"
            color: 0.48, 0.75, 0.92, 1
            halign: "right"
    BoxLayout:
        orientation: "vertical"
        padding: "18dp"
        spacing: "12dp"
        canvas.before:
            Color:
                rgba: 0.10, 0.13, 0.20, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [18]
        Label:
            text: root.mode
            size_hint_y: None
            height: "28dp"
            color: 0.55, 0.78, 0.96, 1
            font_size: "14sp"
        Label:
            text: root.time_text
            font_size: "56sp"
            bold: True
            color: 1, 1, 1, 1
        Label:
            text: "A little progress, consistently."
            size_hint_y: None
            height: "24dp"
            color: 0.65, 0.70, 0.80, 1
        BoxLayout:
            size_hint_y: None
            height: "48dp"
            spacing: "10dp"
            Button:
                text: "Start" if not root.running else "Pause"
                on_release: root.toggle_timer()
                background_normal: ""
                background_color: 0.18, 0.55, 0.78, 1
            Button:
                text: "Reset"
                on_release: root.reset_timer()
                background_normal: ""
                background_color: 0.22, 0.27, 0.37, 1
    BoxLayout:
        size_hint_y: None
        height: "38dp"
        Label:
            text: "[b]Today's tasks[/b]"
            markup: True
            font_size: "18sp"
            halign: "left"
            color: 0.92, 0.95, 1, 1
        Label:
            text: "Saved on this device"
            font_size: "11sp"
            halign: "right"
            color: 0.55, 0.62, 0.72, 1
    BoxLayout:
        size_hint_y: None
        height: "44dp"
        spacing: "8dp"
        TextInput:
            id: task_input
            hint_text: "Add a task..."
            multiline: False
            padding: ["12dp", "10dp"]
            background_color: 0.12, 0.16, 0.23, 1
            foreground_color: 1, 1, 1, 1
            hint_text_color: 0.55, 0.60, 0.70, 1
        Button:
            text: "Add"
            size_hint_x: None
            width: "76dp"
            on_release:
                root.add_task(task_input.text)
                task_input.text = ""
            background_normal: ""
            background_color: 0.20, 0.48, 0.38, 1
    ScrollView:
        do_scroll_x: False
        GridLayout:
            id: task_list
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: "6dp"
    Label:
        text: "FocusFlow starter • Offline-first • More features planned"
        size_hint_y: None
        height: "24dp"
        font_size: "10sp"
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
        self.db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )""")
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
            row = BoxLayout(size_hint_y=None, height="42dp", spacing="8dp",
                            padding=("8dp", "2dp"))
            with row.canvas.before:
                Color(0.12, 0.16, 0.23, 1)
                RoundedRectangle(pos=row.pos, size=row.size, radius=[8])
            row.bind(pos=lambda w, _v: setattr(w.canvas.before.children[-1], "pos", w.pos))
            row.bind(size=lambda w, _v: setattr(w.canvas.before.children[-1], "size", w.size))
            check = CheckBox(active=bool(completed), size_hint_x=None, width="38dp")
            check.bind(active=lambda _w, value, tid=task_id: self.set_task_done(tid, value))
            label = Label(text=title, halign="left", valign="middle",
                          color=(0.55, 0.62, 0.72, 1) if completed else (0.92, 0.95, 1, 1))
            label.bind(size=lambda w, _v: setattr(w, "text_size", w.size))
            row.add_widget(check)
            row.add_widget(label)
            container.add_widget(row)

    def set_task_done(self, task_id, done):
        self.db.execute("UPDATE tasks SET completed=? WHERE id=?",
                        (int(done), task_id))
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
