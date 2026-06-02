from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import get_template
from django.http import HttpResponse
from accounts.decorators import admin_only, pastor_or_admin
from .models import Sermon
from .forms import SermonForm


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    result['Content-Disposition'] = 'attachment; filename="sermon.pdf"'
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
class SermonListView(LoginRequiredMixin, ListView):
    model = Sermon
    template_name = 'sermons/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('q')
        series = self.request.GET.get('series')

        if series:
            qs = qs.filter(series=series)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(speaker__icontains=search) |
                Q(bible_verse__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['current_series'] = self.request.GET.get('series', '')
        ctx['all_series'] = Sermon.objects.values_list('series', flat=True).distinct().exclude(series='')
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(pastor_or_admin, name='dispatch')
class SermonCreateView(LoginRequiredMixin, CreateView):
    model = Sermon
    form_class = SermonForm
    template_name = 'sermons/sermon_form.html'
    success_url = reverse_lazy('sermons:sermon_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Sermon "{self.object.title}" created successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(pastor_or_admin, name='dispatch')
class SermonUpdateView(LoginRequiredMixin, UpdateView):
    model = Sermon
    form_class = SermonForm
    template_name = 'sermons/sermon_form.html'
    context_object_name = 'sermon'

    def get_success_url(self):
        return reverse_lazy('sermons:sermon_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Sermon "{self.object.title}" updated successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class SermonDeleteView(LoginRequiredMixin, DeleteView):
    model = Sermon
    template_name = 'sermons/sermon_confirm_delete.html'
    context_object_name = 'sermon'
    success_url = reverse_lazy('sermons:sermon_list')

    def form_valid(self, form):
        messages.success(self.request, f'Sermon "{self.object.title}" deleted successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SermonDetailView(LoginRequiredMixin, DetailView):
    model = Sermon
    template_name = 'sermons/sermon_detail.html'
    context_object_name = 'sermon'


@method_decorator(login_required, name='dispatch')
class SermonPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        sermon = get_object_or_404(Sermon, pk=pk)
        context = {'sermon': sermon}
        return render_to_pdf('sermon_pdf.html', context)
