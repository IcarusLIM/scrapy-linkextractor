import asyncio


class ExternalLinkExtractor:
    def __init__(self, **kwargs):
        print(kwargs)

    async def extract_links(self, response):
        await asyncio.sleep(3)
        return ["http://www.baidu.com"]
