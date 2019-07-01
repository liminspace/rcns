import json
import fastjsonschema
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy, gettext as _
from .navigator import RouteNavigator
from .validators import route_file_validator


class ImportRoutesForm(forms.Form):
    routes_file = forms.FileField(label=capfirst(gettext_lazy('routes file')),
                                  help_text=gettext_lazy('Upload JSON-file that contains routes with instructions.'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extra_data = {}  # will contain useful data after successful validation

    def clean_routes_file(self):
        f = self.cleaned_data['routes_file']
        if f is None:
            return f

        f.seek(0)
        try:
            data = json.loads(f.read())
        except (TypeError, ValueError, json.JSONDecodeError):
            raise ValidationError(_('Invalid JSON-file.'), code='invalid')

        try:
            route_file_validator(data)  # validate by jsonschema
        except fastjsonschema.JsonSchemaException as e:
            raise ValidationError(_('Invalid file data: %(err_msg)s'), code='invalid', params={'err_msg': e.message})

        for route in data['routes']:
            try:
                # try to parse instructions and get end point
                RouteNavigator(route['instructions'], landmarks_json=route['landmarks']).get_end_point()
            except ValueError as e:
                raise ValidationError(_('Invalid instructions: %(err_msg)s'), code='invalid', params={'err_msg': e})

        self._extra_data['routes_data'] = data
        return f

    def get_routes_data(self):
        return self._extra_data.get('routes_data')


class RouteRequestForm(forms.Form):
    start_point = forms.CharField()
    end_point = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._extra_data = {}  # will contain useful data after successful validation

    @staticmethod
    def _clean_point(val):
        """
        Validate comma-separated int values and return two-items tuple with int values.
        """
        values = val.split(',')
        if len(values) != 2:
            raise ValidationError(_('Invalid point value'))
        try:
            return tuple(int(item.strip()) for item in values)
        except (ValueError, TypeError):
            raise ValidationError(_('Invalid point value'))

    def clean_start_point(self):
        val = self.cleaned_data['start_point']
        self._extra_data['start_point'] = self._clean_point(val)
        return val

    def clean_end_point(self):
        val = self.cleaned_data['end_point']
        self._extra_data['end_point'] = self._clean_point(val)
        return val

    def get_start_point(self):
        return self._extra_data.get('start_point')

    def get_end_point(self):
        return self._extra_data.get('end_point')
