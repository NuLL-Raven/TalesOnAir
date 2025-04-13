class StoreLastURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and not request.path.startswith('/admin/'):
            request.session['last_url'] = request.get_full_path()
        return self.get_response(request)
