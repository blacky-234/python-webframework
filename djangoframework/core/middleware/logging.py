class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Request type check http or ws
        print(f"Request type: {request.scheme}")
        

        # Log the request
        print(f"Request: {request.method} {request.path}")

        response = self.get_response(request)

        #what are in response
        print(f"Response content: {response.content}")
        print(f"Response headers: {response.headers}")
        print(f"Response cookies: {response.cookies}")
        print(f"Response status code: {response.status_code}")
        print("what is dictionary", response.__dict__)

        # Log the response
        print(f"Response: {response.status_code}")

        return response