from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy


# authentication headers
from django.contrib.auth.views import LoginView
# session or roles
from django.contrib.auth.mixins import LoginRequiredMixin

# builtin user creation form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# # Imports for Reordering Feature
# from django.views import View
# from django.shortcuts import redirect
# from django.db import transaction

# from .models import Task
# from .forms import PositionForm


# login view
class CustomLoginView(LoginView):
	template_name='base/login.html'
	fields='__all__'
	redirect_authenticated_user = True
	def get_success_url(self):
		return reverse_lazy('tasks')

# registeration
class RegisterPage(FormView):
	template_name='base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('tasks')
	# register user can login directly
	def form_valid(self,form):
		user=form.save()
		if user is not None:
			login(self.request,user)
		return super(RegisterPage, self).form_valid(form)
	# authenticated user can't see register page
	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage, self).get(*args,**kwargs)




class TaskList(LoginRequiredMixin,ListView):
	model=Task
	context_object_name='tasks'
	# user can only get their datas
	def get_context_data(self, **kwargs):
		context=super().get_context_data(**kwargs)
		# context['color']='red'
		context['tasks']=context['tasks'].filter(user=self.request.user)
		context['count']=context['tasks'].filter(complete=False).count()
		# search task

		search_input=self.request.GET.get('search-area') or ''
		if search_input:
			context['tasks']=context['tasks'].filter(title__contains=search_input)

			# filter by letter starts with
			# context['tasks']=context['tasks'].filter(title__startswith=search_input)
			context['search_input'] = search_input
		return context

class TaskDetail(LoginRequiredMixin,DetailView):
	model=Task
	context_object_name='task'
	template_name='base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
	model=Task
	# fields='__all__'
	fields=['title','description','complete']
	success_url=reverse_lazy('tasks')

	def form_valid(self,form):
		form.instance.user=self.request.user
		return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
	model=Task
	# fields='__all__'
	fields=['title','description','complete']
	success_url=reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
	model=Task
	context_object_name='task'
	success_url=reverse_lazy('tasks')


# class TaskReorder(View):
#     def post(self, request):
#         form = PositionForm(request.POST)

#         if form.is_valid():
#             positionList = form.cleaned_data["position"].split(',')

#             with transaction.atomic():
#                 self.request.user.set_task_order(positionList)

#         return redirect(reverse_lazy('tasks'))

