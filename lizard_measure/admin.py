from django.contrib import admin

from lizard_measure.models import EsfLink
from lizard_measure.models import EsfPattern
from lizard_measure.models import FundingOrganization
from lizard_measure.models import HorizontalBarGraph
from lizard_measure.models import HorizontalBarGraphItem
from lizard_measure.models import KRWStatus
from lizard_measure.models import KRWWatertype
from lizard_measure.models import Measure
from lizard_measure.models import MeasureCategory
from lizard_measure.models import MeasurePeriod
from lizard_measure.models import MeasureStatus
from lizard_measure.models import MeasureStatusMoment
from lizard_measure.models import MeasureType
from lizard_measure.models import MeasuringRod
from lizard_measure.models import Organization
from lizard_measure.models import PredefinedGraphSelection
from lizard_measure.models import Score
from lizard_measure.models import SteeringParameterFree
from lizard_measure.models import SteeringParameterPredefinedGraph
from lizard_measure.models import Unit
from lizard_measure.models import WaterBody
from lizard_measure.models import WatertypeGroup


class MeasureStatusMomentInline(admin.TabularInline):
    model = MeasureStatusMoment


class FundingOrganizationInline(admin.TabularInline):
    model = FundingOrganization


class EsfLinkInline(admin.TabularInline):
    model = EsfLink


class EsfPatternAdmin(admin.ModelAdmin):
    list_filter = [
        'data_set',
        'watertype_group',
    ]


class MeasureInline(admin.TabularInline):
    model = Measure

class SteeringParameterPredefinedGraphAdmin(admin.ModelAdmin):
    pass

class PredefinedGraphSelectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'url', 'for_area_type', 'valid']

class SteeringParameterFreeAdmin(admin.ModelAdmin):
    pass

class MeasureAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'waterbodies',
        'areas',
        'categories',
    ]
    readonly_fields = [
        'datetime_in_source',
        'import_raw',
        'import_source',
    ]
    inlines = [
        MeasureStatusMomentInline, FundingOrganizationInline, EsfLinkInline
    ]


class MeasureStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'color', 'valid']


class MeasureTypeAdmin(admin.ModelAdmin):
    filter_horizontal = ['units']
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'group',
        'klass',
        'subcategory',
        'harmonisation',
        'combined_name',
        'valid',
    ]


class ScoreAdmin(admin.ModelAdmin):
    list_filter = ['measuring_rod', 'area',]
    list_display = [
        'measuring_rod',
        'area',
        'target_2015',
        'target_2027',
        'mep',
        'gep',
        'limit_insufficient_moderate',
        'limit_bad_insufficient',
        'ascending'
    ]


class MeasuringRodAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'parent',
        'code',
        'group',
        'description',
        'measuring_rod',
        'sub_measuring_rod',
        'unit',
        'sign',
        'valid',
    ]


class UnitAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'dimension',
        'conversion_factor',
        'group',
        'valid',
    ]


class KRWStatusAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'valid',
    ]


class MeasurePeriodAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'description',
        'valid',
    ]


class KRWWatertypeAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'group',
        'valid',
    ]


class OrganizationAdmin(admin.ModelAdmin):
    list_display_links = ['description']
    list_display = [
        'code',
        'description',
        'group',
        'source',
        'valid',
    ]


class HorizontalBarGraphItemInline(admin.TabularInline):
    model = HorizontalBarGraphItem

    def formfield_for_dbfield(self, db_field, **kwargs):
        """Trick to make the inline faster:

        http://ionelmc.wordpress.com/2012/01/19/tweaks-for-making-django-admin-faster/
        """
        formfield = super(HorizontalBarGraphItemInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ['location', 'parameter', 'module', 'time_step', 'qualifierset']:
            # dirty trick so queryset is evaluated and cached in .choices
            formfield.choices = formfield.choices
        return formfield


class HorizontalBarGraphAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    inlines = [HorizontalBarGraphItemInline]


admin.site.register(EsfPattern, EsfPatternAdmin)
admin.site.register(FundingOrganization)
admin.site.register(HorizontalBarGraph, HorizontalBarGraphAdmin)
admin.site.register(HorizontalBarGraphItem)
admin.site.register(KRWStatus, KRWStatusAdmin)
admin.site.register(KRWWatertype, KRWWatertypeAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(MeasureCategory)
admin.site.register(MeasurePeriod, MeasurePeriodAdmin)
admin.site.register(MeasureStatus, MeasureStatusAdmin)
admin.site.register(MeasureStatusMoment)
admin.site.register(MeasureType, MeasureTypeAdmin)
admin.site.register(MeasuringRod, MeasuringRodAdmin)
admin.site.register(PredefinedGraphSelection, PredefinedGraphSelectionAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(SteeringParameterFree, SteeringParameterFreeAdmin)
admin.site.register(SteeringParameterPredefinedGraph, SteeringParameterPredefinedGraphAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(WaterBody)
admin.site.register(WatertypeGroup)

