from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import TemplateView
from .helpers import arrayfield_keys_to_values, create_column_defs_list


class DatatablesListView(TemplateView):
    model = None
    queryset = None
    fields = None
    column_names_and_defs = None
    options_list = None
    conditional_show_options_permission = None
    show_options = True
    """
    Formato esperado de options_list, vale aclarar que también puede ser None (En el caso de que sea una tabla
    sin opciones):

    options_list = [
        {
            'label_opcion': string,
            'url_opcion': url de django. string,
            'confirm_modal': Indica si la opción necesita confirmación. boolean, | None
            'parametros_url': lista de parametros a pasar al url. list:string,
            'icono': icono de font awesome (Nombre clase). string, | None
            'permissions': permisos de django requeridos para mostrar esta opción. list:string, | None
            'conditions': [
                                        {
                                            'campo': campo del registro sobre el que se aplica la condición. string,
                                            'valores_verificar': lista de valores para el campo que se verificará que
                                                                 se cumplan. list:string,
                                            'lambda_evaluacion': función lambda que evaluará el campo vs los valores
                                        }+
                                    ] | None
        }+ | None

    ]
    """

    def get_options_list(self):
        if self.options_list is not None:
            for option in self.options_list:
                try:
                    option['label_opcion']
                except KeyError as e:
                    raise ImproperlyConfigured(
                        "%(cls)s necesita el atributo options_list el cual debe contener una lista de diccionarios "
                        "los cuales deben contener entre sus atributos uno llamado label_opcion con un string" % {
                            'cls': self.__class__.__name__
                        }
                    )

                try:
                    option['url_opcion']
                except KeyError as e:
                    raise ImproperlyConfigured(
                        "%(cls)s necesita el atributo options_list el cual debe contener una lista de diccionarios "
                        "los cuales deben contener entre sus atributos uno llamado url_opcion con un string" % {
                            'cls': self.__class__.__name__
                        }
                    )

                try:
                    option['parametros_url']
                except KeyError as e:
                    raise ImproperlyConfigured(
                        "%(cls)s necesita el atributo options_list el cual debe contener una lista de diccionarios "
                        "los cuales deben contener entre sus atributos uno llamado parametros_url con una lista de "
                        "strings que contengan los parametros para la url de la opción" % {
                            'cls': self.__class__.__name__
                        }
                    )

        return self.options_list

    def evaluate_conditions(self, object, permissions, conditions):
        if permissions:
            for permiso in permissions:
                if not self.request.user.has_perm(permiso):
                    return False
        if conditions:
            for condicion in conditions:
                field = condicion['campo']
                valor_field = self.evaluate_data(object, self.model._meta.get_field(field))
                valores_verificar = condicion['valores_verificar']
                lambda_evaluacion = condicion['lambda_evaluacion']
                resultado = lambda_evaluacion(valor_field, valores_verificar)
                if not resultado:
                    return False
        return True

    def get_rendered_urls(self, object):
        rendered_urls = []
        for option_conf in self.get_options_list():
            try:
                permissions = option_conf['permissions']
            except KeyError:
                permissions = None

            try:
                conditions = option_conf['conditions']
            except KeyError:
                conditions = None

            if self.evaluate_conditions(object, permissions, conditions):
                params = []
                for parametro in option_conf['parametros_url']:
                    params.append(self.evaluate_data(object, self.model._meta.get_field(parametro)))
                rendered_urls.append(render_to_string("datatables_tools/url_rendering_tool.html",
                                                      {'name': option_conf['label_opcion'],
                                                       'url': reverse(option_conf['url_opcion'],
                                                                      args=params),
                                                       'icon': option_conf['icono'],
                                                       'confirm_modal': option_conf.get('confirm_modal', None)}))
            else:
                continue
        return rendered_urls

    def get_fields(self):
        if self.fields is None:
            fields = self.model._meta.get_fields()
        else:
            fields = [self.model._meta.get_field(field) for field in self.fields]
        return fields

    def get_all_field_names(self):
        return [field.name for field in self.get_fields()]

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s necesita un QuerySet. Incluya el atributo "
                "%(cls)s.model, %(cls)s.queryset o sobreescriba el método "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset

    def get_filter_and_ordering_criterium(self, field):
        self.criterium = "%s" % field.name
        if field.is_relation or field.many_to_many:
            self.criterium = "%s__id" % (field.name)
        return self.criterium

    def filter_data(self, busqueda):
        busqueda = busqueda.split(" ")
        final_fields = self.get_fields()
        for palabra in busqueda:
            objetos = self.model._default_manager.none()
            for atributo in final_fields:
                choices = atributo.choices
                if choices != []:
                    import re
                    # RECORDAR PROBAR BIEN ESTA LÍNEA CUANDO TODO ESTÉ FUNCIONANDO YA QUE EN EL MOMENTO QUE LA ESCRIBÍ
                    # NO QUEDÉ MUY CONVENCIDO DE QUE HACÍA
                    for llave, valor in choices:
                        if re.search(palabra, valor, re.IGNORECASE):
                            instruccion = "%s" % atributo.name
                            query = {instruccion: llave}
                            objeto = self.get_queryset().filter(**query)
                            if objeto:
                                objetos = objetos | objeto
                else:
                    filter_criterium = self.get_filter_and_ordering_criterium(atributo)
                    instruccion = filter_criterium+"__icontains"
                    query = {instruccion: palabra}
                    objeto = self.get_queryset().filter(**query)
                    if objeto:
                        objetos = objetos | objeto
            if self.queryset:
                self.queryset = self.queryset & objetos
            else:
                self.queryset = objetos

    def set_draw_data_with_params(self, inicio, fin, columna_orden, direccion_orden):
        orden = ''
        if direccion_orden == 'desc':
            orden = "-"
        columna_orden = self.get_filter_and_ordering_criterium(self.model._meta.get_field(columna_orden))
        self.queryset = self.get_queryset().order_by(orden + columna_orden)[inicio:fin]

    def get_draw_parameters(self):
        inicio = int(self.request.GET['start'])
        fin = inicio + int(self.request.GET['length'])
        columna = self.get_all_field_names()[int(self.request.GET['order[0][column]'])]
        direccion = self.request.GET['order[0][dir]']
        return [inicio, fin, columna, direccion]

    def evaluate_data(self, object, field):
        value = None
        if field.choices:
            value = (getattr(object, 'get_%s_display' % field.name)())
        elif field.many_to_many:
            value = getattr(object, field.name)
            if type(value) == list:
                value = ", ".join(value)
            else:
                value = ", ".join([obj.__str__() for obj in getattr(object, field.name).all()])
            return value
        elif field.__class__.__name__ == 'ArrayField':
            choices = field.base_field.choices
            keys = getattr(object, field.name)
            value = ", ".join(arrayfield_keys_to_values(keys, choices))
        else:
            value = getattr(object, field.name)

        return value

    def get_rendered_html_value(self, field, value):
        self.html_value = "<span>%s</span>" % value
        return self.html_value

    def generate_rows(self):
        data = []
        for object in self.get_queryset():
            row = []
            for field in self.get_fields():
                value = self.evaluate_data(object, field)
                value = self.get_rendered_html_value(field, value)
                row.append(value)

            data.append(row)
        return data

    def generate_rows_with_options(self):
        data = []
        for object in self.get_queryset():
            row = []
            for field in self.get_fields():
                value = self.evaluate_data(object, field)
                value = self.get_rendered_html_value(field, value)
                row.append(value)
            opciones = render_to_string("datatables_tools/options_list_rendering_tool.html",
                                        {'urls': self.get_rendered_urls(object)})
            row.append(opciones)

            data.append(row)
        return data

    def generate_final_data(self):
        inicio, fin, columna_orden, direccion_orden = self.get_draw_parameters()
        busqueda = self.request.GET['search[value]']
        final_data = {
            "draw": int(self.request.GET['draw']),
            "recordsTotal": 0,
            "recordsFiltered": 0,
            "data": []
        }

        if busqueda:
            self.filter_data(busqueda)

        cantidad_objetos = self.get_queryset().count()
        final_data['recordsTotal'] = cantidad_objetos
        final_data['recordsFiltered'] = cantidad_objetos
        self.set_draw_data_with_params(inicio, fin, columna_orden, direccion_orden)
        if self.get_options_list():
            final_data['data'] = self.generate_rows_with_options()
        else:
            final_data['data'] = self.generate_rows()
        return final_data

    def get_context_data(self, **kwargs):
        context = super(DatatablesListView, self).get_context_data(**kwargs)
        context['show_options'] = self.show_options

        if self.conditional_show_options_permission:
            if self.request.user.has_perm(self.conditional_show_options_permission):
                context['show_options'] = True
        else:
            context['show_options'] = False

        if self.column_names_and_defs:
            context['column_defs'] = create_column_defs_list(self.column_names_and_defs)
        else:
            context['column_defs'] = create_column_defs_list(self.get_all_field_names())
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            final_data = self.generate_final_data()
            return JsonResponse(final_data)
        else:
            return super(DatatablesListView, self).get(request, *args, **kwargs)
