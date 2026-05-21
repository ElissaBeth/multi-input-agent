import os, time, signal
import numpy as np
import requests
from tools.utils import html_to_discord

class PostDiscordWH:
    def __init__(self, db_folder, name):
        self.db_folder = db_folder
        self.name = name

    ## module
    def load_proc(self, proc_ctrl, proc_status, proc_stop, queue_gen):
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # parent handles shutdown via proc_ctrl/stop_event
        proc_status.put(f"{__name__:<28} starting")

        WEBHOOK_URL = "https://discord.com/api/webhooks/" + os.environ["DISCORD_WH_TOKEN"]
        # proc_stop.wait(timeout=1.0)
        proc_ctrl.value += 1

        # main
        while proc_ctrl.value != 0:
            if proc_stop.wait(timeout=0.1): return
            if not queue_gen.empty():
                text_out = queue_gen.get_nowait()
                text_out = html_to_discord(text_out)
                # proc_status.put(f"{__name__:<28} text_out sent {text_out}")
                # requests.post(WEBHOOK_URL, json={"content": str(text_out)})
                requests.post(WEBHOOK_URL, json={
                    "username": self.name,
                    "embeds": [{"description": text_out}],
                })

if __name__ == '__main__':
    WEBHOOK_URL = "https://discord.com/api/webhooks/" + os.environ["DISCORD_WH_TOKEN"]
    text_out = "Just testing"
    requests.post(WEBHOOK_URL, json={
        "username": "Test00",
        "embeds": [{"description": str(text_out)}],
    })
