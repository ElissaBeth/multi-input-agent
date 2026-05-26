import time, signal, random
import numpy as np

class WriteRndSynopsys:
    def __init__(self, db_folder):
        self.db_folder = db_folder

        self.usr_prompt = 'Write a short synopsys of a news article. ' \
        'Make it a maximum 100 tokens but do not tell me how many you used. ' \
        'Use markup only (no html) to format the text for display. ' \
        'Base the article on the word "{word}".'

        with open(db_folder+'/american-english.txt') as f:
            self.words = [w.strip() for w in f]

    ## module
    def load_proc(self, proc_ctrl, proc_status, proc_stop, queue_ctx):
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # parent handles shutdown via proc_ctrl/stop_event
        proc_status.put(f"{__name__:<28} starting")
        # proc_stop.wait(timeout=2.0)
        proc_ctrl.value += 1

        # main
        while proc_ctrl.value != 0:
            word = random.choice(self.words)
            # proc_status.put(f"{__name__:<28} new word {word}")
            # queue_ctx.put({'role': 'user', 'content': self.usr_prompt.format(word=word)}) # blocks when queue_ctx is full
            queue_ctx.put({'role': 'user', 'content': [{'type': 'text', 'text': self.usr_prompt.format(word=word)}]}) # blocks when queue_ctx is full
            # rnd_spacing = 0.1
            # if random.randint(0, 6) == 0: rnd_spacing = 30.0
            rnd_spacing = random.uniform(10.0, 20.0)
            # rnd_spacing = random.uniform(360.0, 3600.0)
            if proc_stop.wait(timeout=rnd_spacing): return

if __name__ == '__main__':
    obj = WriteRndSynopsys('data')
    print(obj.usr_prompt.format(word=obj.words[100]))
