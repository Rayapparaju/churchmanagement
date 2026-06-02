from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import get_template
from django.http import HttpResponse
from accounts.decorators import admin_only, pastor_or_admin
from .models import PrayerRequest
from .forms import PrayerRequestForm, PrayerUpdateForm


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    result['Content-Disposition'] = 'attachment; filename="prayer_requests.pdf"'
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
class PrayerRequestListView(LoginRequiredMixin, ListView):
    model = PrayerRequest
    template_name = 'prayers/prayer_list.html'
    context_object_name = 'prayer_requests'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        profile = user.profile

        if profile.role in ['admin', 'pastor']:
            return qs

        return qs.filter(
            Q(member=profile.member) | Q(email=user.email)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class PrayerRequestCreateView(CreateView):
    model = PrayerRequest
    form_class = PrayerRequestForm
    template_name = 'prayers/prayer_form.html'
    success_url = reverse_lazy('prayers:prayer_list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            if hasattr(profile, 'member') and profile.member:
                form.instance.member = profile.member
        response = super().form_valid(form)
        messages.success(self.request, 'Your prayer request has been submitted.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(pastor_or_admin, name='dispatch')
class PrayerRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = PrayerRequest
    form_class = PrayerUpdateForm
    template_name = 'prayers/prayer_form.html'
    context_object_name = 'prayer_request'

    def get_success_url(self):
        return reverse_lazy('prayers:prayer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Prayer request updated successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class PrayerRequestDetailView(LoginRequiredMixin, DetailView):
    model = PrayerRequest
    template_name = 'prayers/prayer_detail.html'
    context_object_name = 'prayer_request'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        profile = user.profile

        if profile.role in ['admin', 'pastor']:
            return qs

        return qs.filter(
            Q(member=profile.member) | Q(email=user.email)
        )


@method_decorator(login_required, name='dispatch')
@method_decorator(pastor_or_admin, name='dispatch')
class PrayerRequestPDFView(LoginRequiredMixin, View):
    def get(self, request):
        prayer_requests = PrayerRequest.objects.all()
        context = {'prayer_requests': prayer_requests}
        return render_to_pdf('prayer_pdf.html', context)
