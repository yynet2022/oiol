# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . import apps, models


User = get_user_model()
Action = models.Action
Log = models.Log


class TopView(generic.FormView):
    template_name = apps.AppConfig.name + '/top.html'
    success_url = reverse_lazy('main:top')

    def get_form(self, form_class=None):
        q = Action.objects.filter(action=models.ACTION_IN)

        class _Form(forms.Form):
            def __init__(self, *a, **k):
                for x in q:
                    self.declared_fields.update(
                        {'cb_' + x.user.uid:
                         forms.BooleanField(required=False, initial=False)})
                super().__init__(*a, **k)

        return _Form(**self.get_form_kwargs())

    def form_valid(self, form):
        r = super().form_valid(form)
        for x in form.changed_data:
            if x.startswith('cb_'):
                user = User.objects.get(uid=x.lstrip('cb_'))
                action = getattr(user, 'action', None) or Action(user=user)
                action.setOut()
                action.update_at = timezone.now()
                action.save()
                Log(user=user,
                    message=action.get_action_display()+'*').save()
        return r

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            action = getattr(user, 'action', None) or Action(user=user)
            action.save()

        context['qlist'] = Action.objects.filter(action=models.ACTION_IN).\
            order_by('user__username')
        """
        print(Action.objects.filter(action=models.ACTION_IN).\
              order_by('user__username').query)
        """
        return context


def ToggleView(request, *args, **kwargs):
    v = kwargs.get('action', None)
    if request.user.is_authenticated:
        user = request.user
        action = getattr(user, 'action', None) or Action(user=user)
        if v == models.ACTION_IN:
            action.setIn()
        elif v == models.ACTION_OUT:
            action.setOut()
        action.update_at = timezone.now()
        action.save()
        Log(user=user, message=action.get_action_display()).save()
    return redirect('main:top')


class LogView(generic.ListView):
    template_name = apps.AppConfig.name + '/log.html'
    paginate_by = 50

    class _Paginator(Paginator):
        def validate_number(self, number):
            try:
                n = super().validate_number(number)
            except PageNotAnInteger:
                n = 1
            except EmptyPage:
                n = self.num_pages
            return n

    paginator_class = _Paginator

    def get_queryset(self):
        q = Log.objects.none()
        if self.request.user.is_authenticated:
            q = Log.objects.filter(user=self.request.user).\
                order_by('create_at').reverse()
        return q
