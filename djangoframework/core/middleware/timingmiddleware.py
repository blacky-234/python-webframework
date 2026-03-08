class AsyncTimingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):

        import time
        start_time = time.perf_counter()
        print(f"Start time: {start_time}")
        response = await self.get_response(request)
        duration = await time.perf_counter() - start_time
        print(f"Duration: {duration}")
        response["X-Response-Time"] = f"{duration:.6f}"
        return response