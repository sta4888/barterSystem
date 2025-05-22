from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView, UpdateView, DeleteView, ListView, DetailView, View
)
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Ad, Category, ExchangeProposal




class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/ad_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ['title', 'description', 'image_url', 'category', 'condition']
    template_name = 'ads/ad_form.html'

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy('ads:ad-list')
    template_name = 'ads/ad_confirm_delete.html'

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user


class AdListView(ListView):
    model = Ad
    paginate_by = 10
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        queryset = Ad.objects.all().select_related('category', 'user')
        query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        condition = self.request.GET.get("condition")

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            queryset = queryset.filter(category__id=category)
        if condition:
            queryset = queryset.filter(condition=condition)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['condition_choices'] = Ad.CONDITION_CHOICES

        category = self.request.GET.get('category')
        if category and category.isdigit():
            context['selected_category_id'] = int(category)
        else:
            context['selected_category_id'] = None

        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'




class ExchangeProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    fields = ['ad_sender', 'ad_receiver', 'comment']
    template_name = 'ads/exchange_form.html'
    success_url = reverse_lazy('ads:ad-list')

    def form_valid(self, form):
        form.instance.status = "ожидает"
        return super().form_valid(form)


class ExchangeProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = 'ads/exchange_list.html'
    context_object_name = 'proposals'

    def get_queryset(self):
        qs = ExchangeProposal.objects.all()
        sender = self.request.GET.get("sender")
        receiver = self.request.GET.get("receiver")
        status = self.request.GET.get("status")

        if sender:
            qs = qs.filter(ad_sender__user__id=sender)
        if receiver:
            qs = qs.filter(ad_receiver__user__id=receiver)
        if status:
            qs = qs.filter(status=status)
        return qs


class ExchangeProposalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ExchangeProposal
    fields = ['status']
    template_name = 'ads/exchange_update_form.html'
    success_url = reverse_lazy('ads:exchange-list')

    def test_func(self):
        obj = self.get_object()
        return obj.ad_receiver.user == self.request.user
