# Cloudflare AI Python Wrapper

This is an Async Python wrapper for the Cloudflare AI API. It is a work in progress and is not yet ready for production use.
This does not include all of the Cloudflare AI API endpoints. If you would like to add more, please open a pull request.

If you have any updates or suggestions, please open an issue or pull request. :)

## Installation

```bash
pip install cloudflare-ai
```

## Usage

```python
import asyncio
from CloudflareAI import CloudflareAI


async def main():
    ai = CloudflareAI(
        Cloudflare_API_Key="",
        Cloudflare_Account_Identifier="",
    )
    image = await ai.ImageClassification(
        image_path="image.jpg", model_name="@cf/microsoft/resnet-50"
    )

    text = await ai.TextGeneration(
        prompt="Hello, my name is Alex",
        system_prompt="Hello, my name is Alex",
        model_name="@cf/meta/llama-2-7b-chat-fp16",
        max_tokens=100,
        stream=False,
    )

    image = await ai.TextToImage(
        prompt="A cat on a cloud",
        model_name="@cf/stabilityai/stable-diffusion-xl-base-1.0",
    ) # This will save the image in the current directory as your prompt.


asyncio.run(main())
```
