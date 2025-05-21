from django.contrib import admin

from ads.models import Category, Ad, ExchangeProposal
from users.models import User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    pass

@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    pass