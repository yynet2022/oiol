# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . import apps, models


User = get_user_model()
Action = models.Action


class _Paginator(Paginator):
    def validate_number(self, number):
        try:
            n = super().validate_number(number)
        except PageNotAnInteger:
            n = 1
        except EmptyPage:
            n = self.num_pages
        return n


class _PageRangeMixin(generic.list.MultipleObjectMixin):
    paginator_class = _Paginator
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["is_paginated"]:
            p = context["page_obj"]
            r = p.paginator.get_elided_page_range(
                number=p.number, on_each_side=1, on_ends=1)
            context.update({"page_nav_list": r})
        else:
            context.update({"page_nav_list": None})
        return context


class TopView(_PageRangeMixin, generic.FormView):
    template_name = apps.AppConfig.name + '/top.html'
    object_list = None

    def get_queryset(self):
        return Action.objects.filter(action=models.ACTION_IN).\
            order_by('user__division', 'user__first_name', 'user__last_name')

    def get_form(self, form_class=None):
        s = self.object_list
        q = s if s is not None else self.get_queryset()

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
                user = User.objects.get(uid=x[3:])
                user.action.setOut(by_myself=False)
                user.action.update_at = timezone.now()
                user.action.save()
        return r

    def get_success_url(self):
        p = self.kwargs.get('page') or self.request.GET.get('page') or None
        kwargs = None
        if p is not None:
            kwargs = {'page': p}
        return reverse('main:top', kwargs=kwargs)

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        # print(self.object_list.query)
        return super().get_context_data(**kwargs)


def ToggleView(request, *args, **kwargs):
    v = kwargs.get('action', None)
    if request.user.is_authenticated:
        user = request.user
        action = user.action
        action._setAction(v)
        action.update_at = timezone.now()
        action.save()
    return redirect('main:top')


class LogView(_PageRangeMixin, generic.ListView):
    template_name = apps.AppConfig.name + '/log.html'

    def get_queryset(self):
        q = models.Log.objects.none()
        if self.request.user.is_authenticated:
            q = models.Log.objects.filter(user=self.request.user).\
                order_by('create_at').reverse()
        return q
