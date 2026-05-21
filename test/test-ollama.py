# https://github.com/ollama/ollama-python
# https://docs.ollama.com/api/introduction

from ollama import chat
from ollama import ChatResponse

response:ChatResponse = chat(
    # model='qwen3.5:9b', think=True,
    model='gemma4:e4b', think=True,
    # model='lfm2:24b', think=False,
    stream=False,
    keep_alive=-1,
    messages=[
        {
        'role': 'user',
        'content': 'Write a short (maximum 100 tokens) synopsys of a news article. Use markup only (no html) to format the text for display. Base the article on the word "happy".',
        # 'content': 'Write a very long (maximum 10,000 tokens) story based on the word: happy',
        },
    ]
)
# print(response)
# print(response['message']['content'])
print(response.message.content)
print(f"Done: {response.done}")
print(f"Prompt tokens: {response.prompt_eval_count}")
print(f"Gen tokens: {response.eval_count}")
ts = int(response.eval_count) / (int(response.eval_duration or 0) / 1_000_000_000) if response.eval_count and response.eval_duration else 0.0
print(f"Gen tokens/second: {ts}")
