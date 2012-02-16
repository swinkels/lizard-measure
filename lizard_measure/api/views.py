from django.core.urlresolvers import reverse
from djangorestframework.views import View

from lizard_measure.models import Organization, Measure, Score
from lizard_api.base import BaseApiView

import logging
logger = logging.getLogger(__name__)


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return {
            "measure": reverse("lizard_measure_api_measure"),
            }


class ScoreView(BaseApiView):
    """
    Show organisations for selection and edit
    """
    #todo: add waarde optioneel
    model_class = Score
    field_mapping = {
        'id': 'id',
        'mep': 'mep',
        'gep': 'gep',
        'limit_insufficient_moderate': 'limit_insufficient_moderate',
        'limit_bad_insufficient': 'limit_bad_insufficient',
        'target_2015': 'target_2015',
        'target_2027': 'target_2027',
        'measuring_rod':'measuring_rod__description',
        'area': 'area__name'
    }
    def get_object_for_api(self,
                           score,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
            create object of measure
        """
        model_class = Score
        name_field = 'measuring_rod__description'



        output = {
            'id': score.id,
            'mep': score.mep,
            'gep': score.gep,
            'limit_insufficient_moderate': score.limit_insufficient_moderate,
            'limit_bad_insufficient': score.limit_bad_insufficient,
            'target_2015': score.target_2015,
            'target_2027': score.target_2027,
            'measuring_rod': self._get_related_object(
                score.measuring_rod,
                flat,
            ),
            'area': self._get_related_object(score.area, flat),
        }
        return output


class OrganizationView(BaseApiView):
    """
    Show organisations for selection and edit
    """
    model_class = Organization
    name_field = 'description'

    valid_field='valid'
    valid_value=True

    field_mapping = {
        'id': 'id',
        'code': 'code',
        'description': 'description',
        'group': 'group',
        'source': 'source',
        'read_only': 'source'
    }

    read_only_fields = [
        'code',
        'group',
        'source',
        'read_only'
    ]

    def get_object_for_api(self,
                           org,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
        create object of measure
        """
        if size == self.ID_NAME:
            output = {
                'id': org.id,
                'name': org.description,
            }
        else:
            output = {
                'id': org.id,
                'code': org.code,
                'description': org.description,
                'group': org.group,
                'source': self._get_choice(
                    Organization._meta.get_field('source'),
                    org.source,
                    flat
                ),
                'read_only': org.source > 0
            }
        return output

    def create_objects(self, data):
        """
            overwrite of base api to append code
        """
        success, touched_objects =  super(OrganizationView, self).create_objects(data)

        for object in touched_objects:
            object.code = object.id + 1000
            object.save()

        return success, touched_objects


class MeasureView(BaseApiView):
    """
    Area configuration.
    """
    model_class = Measure
    name_field = 'title'

    valid_field='valid'
    valid_value=True

    field_mapping = {
        'id': 'id',
        'ident': 'ident',
        'title': 'title',
        'is_KRW_measure': 'is_KRW_measure',
        'is_indicator': 'is_indicator',
        'description': 'description',
        'investment_costs': 'investment_costs',
        'exploitation_costs': 'exploitation_costs',
        'responsible_department': 'responsible_department',
        'value': 'value',
        'measure_type': 'measure_type__description',
        'period': 'period__start_date',
        'unit': 'unit__description',
        'initiator': 'initiator__description',
        'executive': 'executive__description',
        'parent': 'parent__title',
        'aggregation_type':  'aggregation_type',
        'read_only': 'read_only',
        'import_raw': 'import_raw',
        'import_source': 'import_source'
    }

    def get_funding_organisations(self, measure):
        """
            returns funding organisation dict

        """

        return [{'id': obj.organization_id,
                 'percentage': obj.percentage,
                 'name': obj.organization.description,
                 'comment': obj.comment}
                for obj in measure.fundingorganization_set.all()]

    def get_object_for_api(self,
                           measure,
                           flat=True,
                           size=BaseApiView.COMPLETE,
                           include_geom=False):
        """
            create object of measure
        """

        output = {}

        if size == self.ID_NAME:
            output = {
                'id': measure.id,
                'name': measure.title,
            }

        if size >= self.SMALL:
            output = {
                'id': measure.id,
                'ident': measure.ident,
                'title': measure.title,
                'is_KRW_measure': measure.is_KRW_measure,
                'is_indicator': measure.is_indicator,
                'description': measure.description,
                'total_costs': measure.total_costs,
                'investment_costs': measure.investment_costs,
                'exploitation_costs': measure.exploitation_costs,
                'responsible_department': measure.responsible_department,
                'value': measure.value,
                'in_sgbp': measure.in_sgbp,
                'measure_type': self._get_related_object(
                    measure.measure_type,
                    flat
                ),
                'period': self._get_related_object(measure.period, flat),
                'unit': self._get_related_object(measure.unit, flat),
                'categories': self._get_related_objects(
                    measure.categories,
                    flat
                ),
                'initiator': self._get_related_object(
                    measure.initiator,
                    flat
                ),
                'executive': self._get_related_object(measure.executive, flat),
                'areas': self._get_related_objects(measure.areas, flat),
                'waterbodies': self._get_related_objects(
                    measure.waterbodies,
                    flat
                ),
                'parent': self._get_related_object(
                    measure.parent,
                    flat
                ),
            }

        if size >= self.MEDIUM:
            output.update({
                'aggregation_type':  self._get_choice(
                    Measure._meta.get_field('aggregation_type'),
                    measure.aggregation_type,
                    flat
                ),
                'funding_organizations': self.get_funding_organisations(
                    measure,
                ),
                'status_moments': measure.get_statusmoments(
                    auto_create_missing_states=True,
                    only_valid=True,
                ),
                'esflink_set': measure.get_esflinks(
                    auto_create_missing_states=True
                ),
            })

        if size >= self.COMPLETE:
            output.update({
                'read_only': measure.read_only, #read only
                'import_raw': measure.import_raw, #read only
                'import_source': measure.get_import_source_display(), #read only
            })

        if include_geom:
            output.update({
                'geom': measure.get_geometry_wkt_string(),
            })

        return output

    def update_many2many(self, record, model_field, name, linked_records):
        """
        update specific part of manyToMany relations.
        input:
        - record: measure
        - model_field. many2many field object
        - linked_records. list with dictionaries with:
            id: id of related objects
            optional some relations in case the relation is through
            another object
        """

        if name == 'funding_organizations':
            record.set_fundingorganizations(linked_records)
        elif name == 'status_moments':
            record.set_statusmoments(linked_records)
        elif name == 'esflink_set':
            record.set_esflinks(linked_records)
        else:
            #areas, waterbodies, category
            self.save_single_many2many_relation(record,
                model_field,
                linked_records,
            )
