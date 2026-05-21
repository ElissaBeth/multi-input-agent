import time, signal, random
import numpy as np
from ollama import chat, ChatResponse, Image

class ModelSingle:
    def __init__(self, db_folder, sys_prompt):
        self.db_folder, self.sys_prompt = db_folder, sys_prompt
        self.model = "gemma4:e4b"

    ## module
    def load_proc(self, proc_ctrl, proc_status, proc_stop, queue_ctx, queue_gen):
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # parent handles shutdown via proc_ctrl/stop_event
        proc_status.put(f"{__name__:<28} starting")

        response: ChatResponse = chat(model=self.model, think=False, stream=False, messages=[{'role': 'system', 'content': ''}]) # wait for model to load into VRAM
        # proc_status.put(f"{__name__:<28} test response {response.message.content}")
        # proc_stop.wait(timeout=3.0)
        proc_ctrl.value += 1 # TODO this is not atomic

        # main
        while proc_ctrl.value != 0:
            if not queue_ctx.empty():
                t1_start = time.perf_counter_ns()
                batch = queue_ctx.get_nowait()
                if isinstance(batch, dict): batch = [batch]
                text_in = dict(batch[-1])
                if isinstance(text_in.get('content'), list):
                    text_parts, images = [], []
                    for block in text_in['content']:
                        if block.get('type') == 'text': text_parts.append(block.get('text', ''))
                        elif block.get('type') == 'image': images.append(block['image'])
                    text_in['content'] = ''.join(text_parts)
                    if images: text_in['images'] = [Image(value=b) for b in images]
                # proc_status.put(f"{__name__:<28} message {text_in}")
                try:
                    response: ChatResponse = chat(
                        model=self.model, think=True, stream=False, keep_alive=-1,
                        messages=[{'role': 'system', 'content': self.sys_prompt}] + [text_in],
                    )
                except Exception as e:
                    proc_status.put(f"{__name__:<28} model call ERROR {e}")
                    return
                text_out = response.message.content
                # proc_status.put(f"{__name__:<28} text in {text_in['content']} out {text_out}")
                t1_time = (time.perf_counter_ns() - t1_start) / 1e9
                # tokens_sec_ollama = response.eval_count / (response.eval_duration / 1e9) if response.eval_count and response.eval_duration else 0.0
                # tokens_sec_real = response.eval_count / t1_time if response.eval_count and t1_time > 0 else 0.0
                # proc_status.put(f"{__name__:<28} tokens  {response.eval_count} qty  {tokens_sec_ollama:6.2f} O t/s {tokens_sec_real:6.2f} R t/s   {text_in['content'][-30:]}")
                queue_gen.put(text_out) # blocks when queue_gen is full

            if proc_stop.wait(timeout=0.1): return

if __name__ == '__main__':
    obj = ModelSingle('data', '')
