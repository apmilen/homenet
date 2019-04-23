import logging

from django.views import View
from django.conf import settings
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse

from penny.utils import ExtendedEncoder

logger = logging.getLogger()


class BaseContextMixin(object):
    title = None               # type: str
    template = 'ui/base.html'  # type: str
    component = None           # type: str
    custom_stylesheet = None   # type: str
    login_required = False     # type: bool

    def user_json(self, request):
        user = request.user
        if not user.is_authenticated:
            return None

        return user.__json__()

    def get_base_context(self, request, *args, **kwargs):
        """get the base context items made available to every template"""

        return {
            'DEBUG': settings.DEBUG,
            # SHA is used to tell sentry which release is running on prod
            'GIT_SHA': settings.GIT_SHA,
            # refers to which set of database settings are used
            # (aka which env is active)
            'ENVIRONMENT': settings.PENNY_ENV,
            'TIME_ZONE': settings.TIME_ZONE,
            'LANGUAGE_CODE': settings.LANGUAGE_CODE,
            'user': request.user,
            'title': self.title or self.__class__.__name__,
            'page_id': self.__class__.__name__.lower(),
            'component': self.component,
            'custom_stylesheet': self.custom_stylesheet,
        }

    def context(self, request, *args, **kwargs):
        """override this in your view to provide extra template context"""
        return {}

    def get_context(self, request, *args, **kwargs):
        """
            assemble the full context dictionary needed to render the
            template (base context + page context)
        """
        context = self.get_base_context(request, *args, **kwargs)
        # the variables used to render the django template

        # update context from View class's context function or attribute
        #   if context is a function, call it to get the dictionary
        #   of actual values
        if hasattr(self.context, '__call__'):
            page_context = self.context(request, *args, **kwargs)
        # if it's alaready a dictionary or property, just use it normally
        elif hasattr(self.context, '__getitem__'):
            page_context = self.context
        else:
            raise TypeError('View.context must be a dictionary or function')
        context.update(page_context)

        return context

    def get_context_data(self, **kwargs):
        context = self.get_context(self.request)
        context.update(kwargs)
        return super().get_context_data(**context)


class HttpResponseWithCallback(HttpResponse):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.callback = kwargs.pop('callback')
        super().__init__(*args, **kwargs)

    def close(self):
        """Trigger a callback after sending the response to the client
        Good for deferring expensive processing that can be done later without
        holding up the response to the client.
        """
        super().close()
        self.callback(request=self.request, response=self)


class APIView(View):
    def respond(self, data=None, errors=None, **kwargs):
        response = {
            'success': not errors,
            'errors': errors or [],
            **(data or {}),
        }
        if errors and 'status' not in kwargs:
            kwargs = {**kwargs, 'status': 500}

        return JsonResponse(response, encoder=ExtendedEncoder, **kwargs)


class BaseView(BaseContextMixin, View):

    def get(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)

        content = loader.render_to_string(self.template, context, request)
        return HttpResponseWithCallback(content, request=request)

    def after_response(self, **kwargs):
        pass


class PublicReactView(BaseView):
    template = 'ui/react_base.html'
    component = 'pages/base.js'
    login_required = False

    def get_base_props(self, request, *args, **kwargs):
        base_props = {
            'url_name': request.resolver_match.url_name,
            'url': request.build_absolute_uri(),
            'domain': request.META.get('HTTP_HOST', ''),
            'view': '.'.join((self.__module__, self.__class__.__name__)),
            'DEBUG': settings.DEBUG,
            # used to tell sentry which release is running on prod
            'GIT_SHA': settings.GIT_SHA,
            # refers to which set of database settings are used
            # (aka which env is active)
            'ENVIRONMENT': settings.PENNY_ENV,
            'TIME_ZONE': settings.TIME_ZONE,
            'user': self.user_json(request),
            'endpoint': settings.ENDPOINT
        }

        return base_props

    def props(self, request, *args, **kwargs):
        """override this in your view to provide extra component props"""
        return {}

    def get_props(self, request, *args, **kwargs):
        # a dict passed to react code
        props = self.get_base_props(request, *args, **kwargs)
        # update props from View class's props function or attribute

        if hasattr(self.props, '__call__'):
            page_props = self.props(request, *args, **kwargs)
        elif hasattr(self.props, '__getitem__'):
            page_props = self.props
        else:
            raise TypeError('View.context must be a dictionary or function')
        props.update(page_props)

        return props

    def get(self, request, *args, **kwargs):
        props = self.get_props(request, *args, **kwargs)
        if request.GET.get('props_json'):
            return JsonResponse(props, encoder=ExtendedEncoder)

        context = self.get_context(request, *args, **kwargs)
        context['props'] = props

        content = loader.render_to_string(self.template, context, request)
        return HttpResponseWithCallback(content,
                                        request=request,
                                        callback=self.after_response)


class ReactView(LoginRequiredMixin, PublicReactView):
    login_url = settings.LOGIN_URL
    login_required = True
