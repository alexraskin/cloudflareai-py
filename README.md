# Cloudflare AI Python Wrapper

This Python library provides a convenient way to interact with the Cloudflare AI API asynchronously, allowing you to leverage the power of Cloudflare's AI models in your applications. With this wrapper, you can easily integrate AI-driven features into your projects without the hassle of handling API requests and responses manually.

## Installation

Install from PyPI:

```bash
pip install cloudflareai
```

Install from Github:

```bash
python -m pip install -U git+https://github.com/alexraskin/cloudflareai-py
```

Or build from source:

```bash
git clone
cd cloudflareai
python setup.py install
```

## Usage

Import the CloudflareAI class and the desired model enums. Then, create an instance of the CloudflareAI class with your Cloudflare API key and account identifier. You can then use the instance to call the desired AI model.

```python
import asyncio

from cloudflareai import (
    CloudflareAI,
    AiTextToImageModels,
    AiTextGenerationModels,
    AiImageClassificationModels,
)


async def main():
    ai = CloudflareAI(
        Cloudflare_API_Key=<Your Token>,
        Cloudflare_Account_Identifier=<Account ID>,
    )

    text = await ai.TextGeneration(
        prompt="You are helpful",
        system_prompt="Hello, my name is Alex",
        model_name=AiTextGenerationModels.CODE_LLAMA_7B,
    )
    image = await ai.TextToImage(
      prompt="a Cat",
      model_name=AiTextToImageModels.XL_BASE
    )
    print(text.text) # returns string
    print(image.image) # returns bytes

    ### Also get status codes
    print(text.status_code)
    print(image.status_code)

asyncio.run(main())
```

## Models

This wrapper also includes enums for AI models, making it easier to select the desired model for your tasks. Available enums include:

- AiImageClassificationModels
- AiTranslationModels
- AiTextGenerationModels
- AiSpeechRecognitionModels
- AiTextToImageModels
- TranslationLanguages

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear description of your changes.

## License

Mozilla Public License Version 2.0 (MPL-2.0) - See LICENSE for more information.
