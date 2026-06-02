import io

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, View

import xhtml2pdf.pisa as pisa

from accounts.decorators import pastor_or_admin
from members.models import Member

from .forms import OfferingForm
from .models import Offering


def render_to_pdf(template_src, context_dict={}):
    html = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@method_decorator(pastor_or_admin, name='dispatch')
class OfferingListView(LoginRequiredMixin, ListView):
    model = Offering
    template_name = 'offerings/offering_list.html'
    context_object_name = 'offerings'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related('member')
        offering_type = self.request.GET.get('offering_type')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        member = self.request.GET.get('member')

        if offering_type:
            qs = qs.filter(offering_type=offering_type)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if member:
            qs = qs.filter(member_id=member)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['offering_types'] = Offering.OFFERING_TYPES
        ctx['members'] = Member.objects.all().order_by('first_name')
        ctx.update({
            k: self.request.GET.get(k, '')
            for k in ['offering_type', 'date_from', 'date_to', 'member']
        })
        return ctx


@method_decorator(pastor_or_admin, name='dispatch')
class OfferingCreateView(LoginRequiredMixin, CreateView):
    model = Offering
    form_class = OfferingForm
    template_name = 'offerings/offering_form.html'
    success_url = reverse_lazy('offerings:list')

    def get_initial(self):
        initial = super().get_initial()
        member_id = self.request.GET.get('member')
        if member_id:
            try:
                initial['member'] = Member.objects.get(pk=member_id)
            except Member.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Offering recorded successfully. Receipt: {self.object.receipt_number}'
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(pastor_or_admin, name='dispatch')
class OfferingDetailView(LoginRequiredMixin, DetailView):
    model = Offering
    template_name = 'offerings/offering_detail.html'
    context_object_name = 'offering'


@method_decorator(pastor_or_admin, name='dispatch')
class OfferingReceiptView(LoginRequiredMixin, DetailView):
    model = Offering

    def get(self, request, *args, **kwargs):
        offering = self.get_object()
        context = {'offering': offering}
        pdf = render_to_pdf('receipt_pdf.html', context)
        if pdf:
            return pdf
        return HttpResponse('PDF generation failed.', status=500)


@method_decorator(pastor_or_admin, name='dispatch')
class OfferingSendWhatsAppView(LoginRequiredMixin, View):
    template_name = 'offerings/offering_whatsapp_compose.html'

    def get(self, request, pk):
        offering = get_object_or_404(Offering, pk=pk)
        return render(request, self.template_name, {
            'offering': offering,
            'message': offering.whatsapp_message(),
        })

    def post(self, request, pk):
        offering = get_object_or_404(Offering, pk=pk)
        custom_message = request.POST.get('message', '').strip()
        if not custom_message:
            messages.error(request, 'Message cannot be empty.')
            return render(request, self.template_name, {
                'offering': offering,
                'message': offering.whatsapp_message(),
            })

        from .services import send_whatsapp
        result = send_whatsapp(offering, custom_message)
        if result['success']:
            messages.success(request, f'WhatsApp receipt sent to {offering.member.full_name()}.')
        else:
            messages.error(request, f'WhatsApp send failed: {result["error"]}')
        return redirect('offerings:detail', pk=pk)
