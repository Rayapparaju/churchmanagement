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
from django.utils import timezone
from accounts.decorators import admin_only
from members.models import Member
from .models import Event
from .forms import EventForm


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    result['Content-Disposition'] = 'attachment; filename="event.pdf"'
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
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events_app/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        timeframe = self.request.GET.get('timeframe')
        search = self.request.GET.get('q')

        if status:
            qs = qs.filter(status=status)
        if timeframe == 'upcoming':
            qs = qs.filter(date__gte=timezone.now().date())
        elif timeframe == 'past':
            qs = qs.filter(date__lt=timezone.now().date())
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = self.request.GET.get('status', '')
        ctx['timeframe'] = self.request.GET.get('timeframe', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events_app/event_form.html'
    success_url = reverse_lazy('events_app:event_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Event "{self.object.title}" created successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events_app/event_form.html'
    context_object_name = 'event'

    def get_success_url(self):
        return reverse_lazy('events_app:event_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Event "{self.object.title}" updated successfully.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_only, name='dispatch')
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events_app/event_confirm_delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events_app:event_list')

    def form_valid(self, form):
        messages.success(self.request, f'Event "{self.object.title}" deleted successfully.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'events_app/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_is_volunteer'] = self.request.user.is_authenticated and (
            Member.objects.filter(user=self.request.user, volunteered_events=self.object).exists()
        )
        return ctx


@method_decorator(login_required, name='dispatch')
class EventPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        context = {'event': event}
        return render_to_pdf('event_pdf.html', context)


@method_decorator(login_required, name='dispatch')
class VolunteerForEventView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            messages.error(request, 'Only registered members can volunteer for events.')
            return redirect('events_app:event_detail', pk=pk)

        if member in event.volunteers.all():
            event.volunteers.remove(member)
            messages.info(request, f'You have been removed from volunteers for "{event.title}".')
        else:
            event.volunteers.add(member)
            messages.success(request, f'You have volunteered for "{event.title}". Thank you!')

        return redirect('events_app:event_detail', pk=pk)
