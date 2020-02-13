from django.contrib import admin

from dbLayer.models import OrgNodeTypes


@admin.register(OrgNodeTypes)
class OrgNodeTypesAdmin(admin.ModelAdmin):
    list_display = ('client', 'node_type', 'description', 'del_ind')
    fields = (('client', 'node_type'), 'description')
    list_filter = ('client',)
