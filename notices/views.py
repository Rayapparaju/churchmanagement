from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from accounts.decorators import admin_only, pastor_or_admin
from .models import Notice
from .forms import NoticeForm


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    result['Content-Disposition'] = 'attachment; filename="notices.pdf"'
    result['Content-Transfer-Encoding'] = 'binary'

    from io import BytesIO
    from xhtml2pdf import pisa

    buf = BytesIO()
    pisa_status = pisa.pisaDocument(BytesIO(html.encode('utf-8')), buf)
    if pisa_status.err:
        return HttpResponse('PDF generation error', content_type='text/plain')
    result.write(buf.getvalue())
    buf.close()
    return result


@method_decorator(login_required, name='dispatch')
class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'admin':
            qs = Notice.objects.all()
        else:
            qs = Notice.objects.filter(is_active=True)
        return qs.order_by('-is_pinned', '-created_at')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/notice_form.html'
    success_url = reverse_lazy('notices:notice_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Notice "{self.object.title}" created successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class NoticeUpdateView(LoginRequiredMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/notice_form.html'
    context_object_name = 'notice'

    def get_success_url(self):
        return reverse_lazy('notices:notice_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Notice "{self.object.title}" updated successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class NoticeDeleteView(LoginRequiredMixin, DeleteView):
    model = Notice
    template_name = 'notices/notice_confirm_delete.html'
    context_object_name = 'notice'
    success_url = reverse_lazy('notices:notice_list')

    def form_valid(self, form):
        messages.success(self.request, f'Notice "{self.object.title}" deleted successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NoticeDetailView(LoginRequiredMixin, DetailView):
    model = Notice
    template_name = 'notices/notice_detail.html'
    context_object_name = 'notice'


@method_decorator(login_required, name='dispatch')
class NoticePDFView(LoginRequiredMixin, View):
    def get(self, request):
        notices = Notice.objects.filter(is_active=True).order_by('-is_pinned', '-created_at')
        context = {'notices': notices}
        return render_to_pdf('notice_pdf.html', context)
