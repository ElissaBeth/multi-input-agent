import os, requests

WEBHOOK_URL = "https://discord.com/api/webhooks/" + os.environ["DISCORD_WH_TOKEN"]

# requests.post(WEBHOOK_URL, json={"content": "Hello from Python!"})

# # Custom username and avatar for the message
# requests.post(WEBHOOK_URL, json={
#     "content": "I can pretend to be anyone",
#     "username": "Trade Bot",
#     "avatar_url": "https://example.com/some-avatar.png"
# })

# Embeds for richer formatting
requests.post(WEBHOOK_URL, json={
    "embeds": [{
        "title": "Deploy Complete",
        "description": "v2.4.1 is live on production",
        "color": 0x00FF00,  # green sidebar
        "fields": [
            {"name": "Environment", "value": "prod", "inline": True},
            {"name": "Duration", "value": "43s", "inline": True}
        ]
    }]
})

# # using the new components
# requests.post(
#     f"{WEBHOOK_URL}?with_components=true",
#     json={
#         "flags": 32768,  # IS_COMPONENTS_V2
#         "components": [
#             {
#                 "type": 17,  # Container
#                 "accent_color": 0x1DA1F2,  # blue sidebar
#                 "components": [
#                     {
#                         "type": 9,  # Section
#                         "components": [
#                             {
#                                 "type": 10,  # TextDisplay
#                                 "content": "**Breaking: OpenAI Announces GPT-5**"
#                             },
#                             {
#                                 "type": 10,
#                                 "content": "The new model reportedly doubles reasoning benchmarks and introduces native multimodal generation."
#                             }
#                         ],
#                         "accessory": {
#                             "type": 11,  # Thumbnail
#                             "media": {
#                                 "url": "https://example.com/article-thumb.jpg"
#                             }
#                         }
#                     },
#                     {
#                         "type": 14,  # Separator
#                         "divider": True,
#                         "spacing": 1  # small
#                     },
#                     {
#                         "type": 10,  # TextDisplay
#                         "content": "-# via TechCrunch • April 6, 2026"
#                     }
#                 ]
#             }
#         ]
#     }
# )
