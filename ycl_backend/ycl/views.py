from django.http import HttpResponse

# シンプルなビューを作成
def index(request):
    return HttpResponse("Hello, world.")