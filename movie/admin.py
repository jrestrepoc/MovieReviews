from django.contrib import admin
from .models import Movie, Newsletter

# Registro del modelo Movie existente
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year')
    list_filter = ('genre', 'year')
    search_fields = ('title', 'genre')
    list_per_page = 20

# Registro del modelo Newsletter
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email',)
    readonly_fields = ('subscribed_date',)
    list_per_page = 50
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} suscripciones han sido activadas.')
    activate_subscriptions.short_description = "Activar suscripciones seleccionadas"
    
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} suscripciones han sido desactivadas.')
    deactivate_subscriptions.short_description = "Desactivar suscripciones seleccionadas"