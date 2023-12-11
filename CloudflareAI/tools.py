from starlette.responses import StreamingResponse


async def process_streaming_response(response: StreamingResponse):
    async for chunk in response.body_iterator:
        print(chunk)
