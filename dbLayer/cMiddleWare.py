class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        res = self.get_response(request)
        res["Access-Control-Allow-Origin"] = "*"
        res["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return res
