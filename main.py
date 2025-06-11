from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from jnius import autoclass
import os

Window.clearcolor = (1, 1, 1, 1)

class MonitorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.url_input = TextInput(hint_text="Enter one or more URLs (one per line)", multiline=True, size_hint_y=0.3)
        self.start_btn = Button(text="Start Monitoring", on_press=self.start_service)
        self.stop_btn = Button(text="Stop Monitoring", on_press=self.stop_service)
        self.view_log_btn = Button(text="View Change Log", on_press=self.view_log)

        self.log_display = Label(text="", size_hint_y=None)
        self.scroll = ScrollView(size_hint=(1, 0.5))
        self.scroll.add_widget(self.log_display)

        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.start_btn)
        self.layout.add_widget(self.stop_btn)
        self.layout.add_widget(self.view_log_btn)
        self.layout.add_widget(self.scroll)

        return self.layout

    def start_service(self, instance):
        urls = self.url_input.text.strip()
        if not urls:
            return

        with open("/storage/emulated/0/monitor_urls.txt", "w") as f:
            f.write(urls)

        if os.path.exists("/storage/emulated/0/stop_monitoring.txt"):
            os.remove("/storage/emulated/0/stop_monitoring.txt")

        service = autoclass("org.kivy.android.PythonService")
        context = autoclass("org.kivy.android.PythonActivity").mActivity
        service.start(context, "")
        print("Service started.")

    def stop_service(self, instance):
        with open("/storage/emulated/0/stop_monitoring.txt", "w") as f:
            f.write("stop")

    def view_log(self, instance):
        log_path = "/storage/emulated/0/monitor_log.txt"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                self.log_display.text = f.read()
        else:
            self.log_display.text = "No changes detected yet."

if __name__ == "__main__":
    MonitorApp().run()
