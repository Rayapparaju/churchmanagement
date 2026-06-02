import io
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, View

import xhtml2pdf.pisa as pisa

from accounts.decorators import pastor_or_admin
from members.models import Staff

from .forms import AttendanceForm, BulkAttendanceForm
from .models import Attendance


def render_to_pdf(template_src, context_dict={}):
    html = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@method_decorator(pastor_or_admin, name='dispatch')
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related('staff')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        event_type = self.request.GET.get('event_type')
        staff = self.request.GET.get('staff')

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if event_type:
            qs = qs.filter(event_type=event_type)
        if staff:
            qs = qs.filter(staff_id=staff)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event_types'] = Attendance.EVENT_TYPES
        ctx['staff_list'] = Staff.objects.filter(is_active=True).order_by('first_name')
        ctx['today'] = date.today()
        return ctx


@method_decorator(pastor_or_admin, name='dispatch')
class MarkAttendanceView(LoginRequiredMixin, FormView):
    template_name = 'attendance/mark_attendance.html'
    form_class = BulkAttendanceForm
    success_url = reverse_lazy('attendance:attendance_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event_types'] = Attendance.EVENT_TYPES
        ctx['staff_list'] = Staff.objects.filter(is_active=True).order_by('first_name')
        ctx['today'] = date.today()
        return ctx

    def form_valid(self, form):
        event_type = form.cleaned_data['event_type']
        attendance_date = form.cleaned_data['date']
        selected_staff = form.cleaned_data['staff_members']

        created_count = 0
        for staff in selected_staff:
            _, created = Attendance.objects.get_or_create(
                staff=staff,
                event_type=event_type,
                date=attendance_date,
                defaults={'attended': True},
            )
            if created:
                created_count += 1

        messages.success(
            self.request,
            f'Attendance marked for {created_count} staff member(s) on {attendance_date}.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


@method_decorator(pastor_or_admin, name='dispatch')
class AttendanceReportView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_report.html'
    context_object_name = 'attendances'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset().select_related('staff')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        event_type = self.request.GET.get('event_type')
        staff = self.request.GET.get('staff')

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if event_type:
            qs = qs.filter(event_type=event_type)
        if staff:
            qs = qs.filter(staff_id=staff)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['event_types'] = Attendance.EVENT_TYPES
        ctx['staff_list'] = Staff.objects.filter(is_active=True).order_by('first_name')
        qs = self.get_queryset()
        total = qs.count()
        present = qs.filter(attended=True).count()
        ctx['total_records'] = total
        ctx['total_attended'] = present
        ctx['summary'] = {
            'total': total,
            'present': present,
            'absent': total - present,
        }
        ctx.update({
            k: self.request.GET.get(k, '')
            for k in ['date_from', 'date_to', 'event_type', 'staff']
        })
        return ctx


@pastor_or_admin
@login_required
def attendance_report_pdf(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    event_type = request.GET.get('event_type')
    staff = request.GET.get('staff')

    qs = Attendance.objects.select_related('staff').all()
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)
    if event_type:
        qs = qs.filter(event_type=event_type)
    if staff:
        qs = qs.filter(staff_id=staff)

    context = {
        'attendances': qs,
        'total_records': qs.count(),
        'total_attended': qs.filter(attended=True).count(),
        'date_from': date_from,
        'date_to': date_to,
        'event_type': event_type,
    }
    pdf = render_to_pdf('attendance_pdf.html', context)
    if pdf:
        return pdf
    return HttpResponse('PDF generation failed.', status=500)
