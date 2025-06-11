import time
import urllib.request
from plyer import notification
import os

def read_urls():
    try:
        with open("/storage/emulated/0/monitor_urls.txt", "r") as f:
            return [url.strip() for url in f.readlines() if url.strip()]
    except:
        return []

def send_notification(url):
    notification.notify(
        title="Website Changed!",
        message=f"Change detected on {url}",
        timeout=5
    )

def log_change(url):
    with open("/storage/emulated/0/monitor_log.txt", "a") as f:
        f.write(f"[{time.ctime()}] Change detected on {url}\n")

def should_stop():
    return os.path.exists("/storage/emulated/0/stop_monitoring.txt")

def monitor():
    urls = read_urls()
    if not urls:
        return

    last_contents = {url: None for url in urls}

    while not should_stop():
        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=5) as response:
                    html = response.read()

                if last_contents[url] is not None and html != last_contents[url]:
                    send_notification(url)
                    log_change(url)

                last_contents[url] = html
            except:
                pass

        time.sleep(1)

if __name__ == "__main__":
    monitor()
