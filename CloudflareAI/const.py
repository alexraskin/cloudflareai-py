class CloudflareAIConst:
    def __init__(self):
        ...

    @property
    def AiTextGenerationModels(self) -> list:
      """
      Returns a list of all available text generation models.
      """
      return [
          "@cf/meta/llama-2-7b-chat-fp16",
          "@cf/meta/llama-2-7b-chat-int8",
          "@cf/mistral/mistral-7b-instruct-v0.1",
          "@hf/thebloke/codellama-7b-instruct-awq",
        ]
    
    @property
    def AiSpeechRecognitionModels(self) -> list:
      """
      Returns a list of all available speech recognition models.
      """
      return ["@cf/openai/whisper"]
    
    @property
    def AiTranslationModels(self) -> list:
      """
      Returns a list of all available translation models.
      """
      return ["@cf/meta/m2m100-1.2b"]
    
    @property
    def AiImageClassificationModels(self) -> list:
      """
      Returns a list of all available image classification models.
      """
      return ["@cf/microsoft/resnet-50"]
    
    @property
    def AiTextToImageModels(self) -> list:
      """
      Returns a list of all available text to image models.
      """
      return ["@cf/stabilityai/stable-diffusion-xl-base-1.0"]
    
    @property
    def TranslationLanguages(self) -> list:
      """
      Returns a list of all available translation languages.
      """
      return [
        "english",
        "chinese",
        "french",
        "spanish",
        "arabic",
        "russian",
        "german",
        "japanese",
        "portuguese",
        "hindi",
      ]
