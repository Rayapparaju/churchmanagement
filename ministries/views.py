from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

import xhtml2pdf.pisa as pisa

from accounts.decorators import admin_only, pastor_or_admin

from .forms import MinistryForm
from .models import Ministry


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@method_decorator(login_required, name='dispatch')
class MinistryListView(LoginRequiredMixin, ListView):
    model = Ministry
    template_name = 'ministries/ministry_list.html'
    context_object_name = 'ministries'


@method_decorator(pastor_or_admin, name='dispatch')
class MinistryCreateView(LoginRequiredMixin, CreateView):
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/ministry_form.html'
    success_url = reverse_lazy('ministries:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Ministry "{self.object.name}" created successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(pastor_or_admin, name='dispatch')
class MinistryUpdateView(LoginRequiredMixin, UpdateView):
    model = Ministry
    form_class = MinistryForm
    template_name = 'ministries/ministry_form.html'
    context_object_name = 'ministry'

    def get_success_url(self):
        return reverse_lazy('ministries:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Ministry "{self.object.name}" updated successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(admin_only, name='dispatch')
class MinistryDeleteView(LoginRequiredMixin, DeleteView):
    model = Ministry
    template_name = 'ministries/ministry_confirm_delete.html'
    context_object_name = 'ministry'
    success_url = reverse_lazy('ministries:list')

    def form_valid(self, form):
        messages.success(self.request, f'Ministry "{self.object.name}" deleted successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class MinistryDetailView(LoginRequiredMixin, DetailView):
    model = Ministry
    template_name = 'ministries/ministry_detail.html'
    context_object_name = 'ministry'


@method_decorator(login_required, name='dispatch')
class MinistryMemberPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        ministry = Ministry.objects.prefetch_related('members').get(pk=pk)
        context = {
            'ministry': ministry,
            'members': ministry.members.all(),
        }
        pdf = render_to_pdf('ministry_pdf.html', context)
        if pdf:
            return pdf
        return HttpResponse('PDF generation failed.', status=500)
