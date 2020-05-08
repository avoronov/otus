from courses.forms import MessageForm
from courses.models import Course
from courses.tasks import task_send_email
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView


class CourseListView(ListView):
    model = Course

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).all()


class CourseCreateView(CreateView):
    model = Course
    success_url = reverse_lazy('courses:list')
    fields = ['title', 'description', 'teacher']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Добавить новый курс'
        return context


class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title  # TODO: title doesn't passed to template, why?
        return context


class CourseUpdateView(UpdateView):
    model = Course
    success_url = reverse_lazy('courses:list')  # TODO: how to get pk from request for building url for course:view?
    fields = ['title', 'description', 'teacher']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class MessageView(FormView):
    template_name = 'courses/send_message.html'
    form_class = MessageForm
    success_url = reverse_lazy('courses:list')

    def form_valid(self, form):
        task_send_email.delay(form.cleaned_data['email'], form.cleaned_data['title'], form.cleaned_data['message'])
        return super().form_valid(form)
