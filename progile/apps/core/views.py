from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
class HomeView(View):
	template_name = 'home.html'

	def get(self, request, *args, **kwargs):

		return render(request, self.template_name)