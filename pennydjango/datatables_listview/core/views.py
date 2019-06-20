from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse

from .utils import (
    generate_q_objects_by_fields_and_words, arrayfield_keys_to_values,
    create_column_defs_list, Draw
)


class DatatablesListView:
    """
    Author: Milton Lenis
    Date: 16 April 2017
    View implementation for datatables_listview
    """
    model = None
    queryset = None
    fields = None
    options_list = []
    show_options = True
    show_options_permission = None
    perms_manager = None
    column_names_and_defs = None
    table_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.model is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Model. Define "
                "%(cls)s.model" % {
                    'cls': self.__class__.__name__
                }
            )

        for option in self.options_list:
            try:
                option['option_label']
            except KeyError:
                raise ImproperlyConfigured(
                    "%(cls)s needs options_list attr created in the __init__ "
                    "method. It must be a list of dictionaries with and key"
                    "called 'option_label' with a string" % {
                        'cls': self.__class__.__name__
                    }
                )
            try:
                option['option_url']
            except KeyError:
                raise ImproperlyConfigured(
                    "%(cls)s needs options_list attr created in the __init__ "
                    "method. It must be a list of dictionaries with and key"
                    "called 'option_url' with a string" % {
                        'cls': self.__class__.__name__
                    }
                )

            try:
                option['url_params']
            except KeyError:
                raise ImproperlyConfigured(
                    "%(cls)s needs options_list attr created in the __init__ "
                    "method. It must be a list of dictionaries with and key"
                    "called 'url_params' with a list of parameters of the "
                    "url_option as string" % {
                        'cls': self.__class__.__name__
                    }
                )

    def get_options_list(self):
        return self.options_list

    def get_queryset(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to get the queryset or generate one with the model

        Juan Diego: Simplified and cached queryset
        """
        if self.queryset:
            return self.queryset

        self.queryset = self.model._default_manager.all()
        return self.queryset

    def get_fields(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to get all the field instances using the Django's Model _meta API

        Juan Diego: Simplified the method
        """
        if self.fields:
            for field in self.fields:
                yield self.model._meta.get_field(field)
        return self.model._meta.get_fields()

    def get_field_names(self):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to get the fields definition for this listview

        Juan Diego: Use get_fields instead
        """
        if self.fields:
            return self.fields
        return [field.name for field in self.get_fields()]

    def get_draw_parameters(self, request):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to extract the draw parameters from the request, those
        parameters are sent by datatables server-side
        """

        start = int(request.GET.get('start', 0))
        end = start + int(request.GET.get('length', 0))

        column = int(request.GET.get('order[0][column]', 0))
        field_names = self.get_field_names()
        sort_column = field_names[column]

        sort_order = request.GET.get('order[0][dir]', "")
        search = request.GET.get('search[value]', "")
        draw = int(request.GET.get('draw', 0))

        return Draw(start, end, sort_column, sort_order, search, draw)

    def filter_by_search_text(self, queryset, search_text):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to filter the queryset given a search_text. This filters the
        queryset by each one of the fields doing icontains lookup and spliting
        the search_text into words
        """
        # First we need to generate Q objects to do the filtering all over the
        # queryset
        q_objects = generate_q_objects_by_fields_and_words(
            self.get_fields(),
            search_text
        )
        return queryset.filter(q_objects)

    def filter_by_draw_parameters(self, queryset, draw_parameters):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method ot filter the queryset with the draw parameters, this returns the
        queryset sorted (Depending of the order) by a column and slices the
        queryset by a start position and end position
        """
        sort_order = ""
        if draw_parameters.sort_order == "desc":
            sort_order = "-"
        sort_criteria = "{0}{1}".format(sort_order, draw_parameters.sort_column)
        return queryset.order_by(sort_criteria)[draw_parameters.start:draw_parameters.end]

    def generate_rows(self, queryset=None):
        queryset = queryset or self.get_queryset()
        data = []
        for obj in queryset:
            row = []
            for field in self.get_fields():
                value = self.evaluate_data(obj, field)
                value = self.get_rendered_html_value(value)
                row.append(value)

            data.append(row)
        return data

    def evaluate_data(self, obj, field):
        if field.choices:
            value = getattr(obj, 'get_%s_display' % field.name)()
        elif field.many_to_many:
            value = getattr(obj, field.name)
            if type(value) == list:
                value = ", ".join(value)
            else:
                qs_objects = getattr(obj, field.name).all()
                value = ", ".join([str(obj) for obj in qs_objects])
            return value
        elif field.__class__.__name__ == 'ArrayField':
            choices = field.base_field.choices
            keys = getattr(obj, field.name)
            value = ", ".join(arrayfield_keys_to_values(keys, choices))
        else:
            value = getattr(obj, field.name)

        return value

    def get_rendered_html_value(self, value):
        return "<span>%s</span>" % value

    def generate_data(self, request):
        """
        Author: Milton Lenis
        Date: 16 April 2017
        Method to generate the final data required for the JsonResponse,
        it returns a dictionary with the data formated as datatables requires it
        """
        draw_parameters = self.get_draw_parameters(request)
        queryset = self.get_queryset()

        if draw_parameters.search:
            queryset = self.filter_by_search_text(queryset, draw_parameters.search)

        objects_count = queryset.count()
        # This uses the 'filter_by_draw_params' to filter the queryset according
        # with the draw parameters
        # This means: it's the filter for the displaying page of the datatable
        queryset = self.filter_by_draw_parameters(queryset, draw_parameters)
        if self.get_options_list():
            generated_rows = self.generate_rows_with_options()
        else:
            generated_rows = self.generate_rows(queryset)
        return {
            'draw': draw_parameters.draw,
            'recordsTotal': objects_count,
            'recordsFiltered': objects_count,
            'data': generated_rows
        }

    def get(self, request, *args, **kwargs):
        """
        Author: Milton Lenis
        Date: April 16 2017
        If the request is ajax it returns the requested data as a JSON, if not,
        it calls the super to give a normal http response and show the template
        """
        if request.is_ajax():
            final_data = self.generate_data(request)
            return JsonResponse(final_data)
        else:
            return super(DatatablesListView, self).get(request, *args, **kwargs)

    def has_user_permission(self, permission):
        user = self.request.user
        if user.is_authenticated:
            if self.perms_manager:
                manager = getattr(user, self.perms_manager)
                return getattr(manager, permission)
        return False

    def get_context_data(self, **kwargs):
        context = super(DatatablesListView, self).get_context_data(**kwargs)
        context['show_options'] = self.show_options
        if self.show_options_permission:
            context['show_options'] = self.has_user_permission(
                self.show_options_permission
            )

        if self.column_names_and_defs:
            context['column_defs'] = create_column_defs_list(
                self.column_names_and_defs
            )
        else:
            context['column_defs'] = create_column_defs_list(
                self.get_field_names()
            )

        context['table_name'] = self.table_name
        return context
