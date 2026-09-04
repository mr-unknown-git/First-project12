# filename="main.py"
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
import httpx
import random
import threading
import time
from urllib.parse import urlparse

class TikTokViewBot(App):
    def build(self):
        self.title = "TikTok View Bot (2026)"
        self.views_sent = 0
        self.running = False

        # Main layout
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # URL Input
        layout.add_widget(Label(text="TikTok Video URL:"))
        self.url_input = TextInput(hint_text="https://www.tiktok.com/@user/video/123...")
        layout.add_widget(self.url_input)

        # Proxy Input
        layout.add_widget(Label(text="Proxy List (one per line):"))
        self.proxy_input = TextInput(hint_text="http://user:pass@ip:port\nsocks5://user:pass@ip:port")
        layout.add_widget(self.proxy_input)

        # Threads
        layout.add_widget(Label(text="Threads:"))
        self.thread_spinner = Spinner(text="10", values=("5", "10", "20", "50"))
        layout.add_widget(self.thread_spinner)

        # Start/Stop Button
        self.start_button = Button(text="START BOT", background_color=(0, 1, 0, 1))
        self.start_button.bind(on_press=self.toggle_bot)
        layout.add_widget(self.start_button)

        # Status Label
        self.status_label = Label(text="Status: Idle", font_size=20)
        layout.add_widget(self.status_label)

        # View Counter
        self.counter_label = Label(text="Views Sent: 0", font_size=20)
        layout.add_widget(self.counter_label)

        return layout

    def toggle_bot(self, instance):
        if not self.running:
            self.start_bot()
        else:
            self.stop_bot()

    def start_bot(self):
        self.running = True
        self.start_button.text = "STOP BOT"
        self.start_button.background_color = (1, 0, 0, 1)
        self.status_label.text = "Status: Running..."

        # Get inputs
        video_url = self.url_input.text.strip()
        proxy_list = [p.strip() for p in self.proxy_input.text.split("\n") if p.strip()]
        threads = int(self.thread_spinner.text)

        # Start worker threads
        for _ in range(threads):
            t = threading.Thread(target=self.worker, args=(video_url, proxy_list))
            t.daemon = True
            t.start()

    def stop_bot(self):
        self.running = False
        self.start_button.text = "START BOT"
        self.start_button.background_color = (0, 1, 0, 1)
        self.status_label.text = "Status: Stopped"

    def worker(self, video_url, proxy_list):
        video_id = self.get_video_id(video_url)
        if not video_id:
            self.status_label.text = "Error: Invalid URL"
            return

        while self.running:
            proxy = random.choice(proxy_list) if proxy_list else None
            success = self.send_view(video_id, proxy)
            if success:
                self.views_sent += 1
                Clock.schedule_once(self.update_counter)
            time.sleep(random.uniform(0.5, 2.0))

    def get_video_id(self, url):
        try:
            parsed = urlparse(url)
            if "vm.tiktok.com" in parsed.netloc or "vt.tiktok.com" in parsed.netloc:
                with httpx.Client(follow_redirects=True) as client:
                    r = client.get(url, headers={"User-Agent": random.choice(self.get_user_agents())})
                    url = str(r.url)
            return url.split("/video/")[-1].split("?")[0]
        except:
            return None

    def send_view(self, video_id, proxy):
        user_agents = self.get_user_agents()
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.tiktok.com/",
        }

        try:
            with httpx.Client(proxies=proxy, timeout=15, http2=True) as client:
                # Get video metadata
                meta = client.get(
                    f"https://www.tiktok.com/api/v2/video/{video_id}/meta/",
                    headers=headers
                )
                if meta.status_code != 200:
                    return False

                # Send view
                data = {
                    "video_id": video_id,
                    "play_duration": random.randint(3, 10),
                    "is_fullscreen": random.choice([0, 1]),
                    "is_muted": random.choice([0, 1]),
                }
                r = client.post(
                    f"https://www.tiktok.com/api/v2/video/{video_id}/view/",
                    json=data,
                    headers=headers
                )
                return r.status_code == 200
        except:
            return False

    def get_user_agents(self):
        return [
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 12; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; moto g(10) power) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        ]

    def update_counter(self, dt):
        self.counter_label.text = f"Views Sent: {self.views_sent}"

if __name__ == "__main__":
    TikTokViewBot().run()
