from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

from .forms import PrettyPrintForm

class PrettyPrintView(View):
    template_name = 'abc.html'
    test_msg = 'This is a test2 msg.'

    def get(self, request):
        return render(request, 'tools/pretty_print.html', {'form': PrettyPrintForm})

    def post(self, request):
        return HttpResponse("It is working")
