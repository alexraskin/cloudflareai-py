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

from CloudflareAI import CloudflareAI, AiTextToImageModels, AiTextGenerationModels, AiImageClassificationModels


async def main():
    ai = CloudflareAI(
        Cloudflare_API_Key=<Your Token>,
        Cloudflare_Account_Identifier=<Account ID>,
    )
    image = await ai.ImageClassification(
        image_path="image.jpg", model_name=AiImageClassificationModels.RESNET_50
    )

    text = await ai.TextGeneration(
        prompt="You are helpful",
        system_prompt="Hello, my name is Alex",
        model_name=AiTextGenerationModels.CODE_LLAMA_7B,
    )
    image = await ai.TextToImage(prompt="a Cat", model_name=AiTextToImageModels.XL_BASE)

asyncio.run(main())
```

## License

Mozilla Public License Version 2.0 (MPL-2.0) - See LICENSE for more information.
