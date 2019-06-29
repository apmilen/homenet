from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.perms.has_admin_access()


class AgentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.perms.has_agent_access()


class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.perms.has_client_access()


class ClientOrAgentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.perms.has_client_or_agent_access()


class MainObjectContextMixin:
    pk_url_kwarg = 'pk'
    main_model = None
    context_name = 'main_object'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_object = None
        self.main_object_qs = None

    def get(self, request, *args, **kwargs):
        self.main_object = self.get_main_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.main_object = self.get_main_object()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except AttributeError:
            context = {}
        context[self.context_name] = self.get_main_object()
        return context

    def get_main_object_qs(self):
        self.main_object_qs = self.main_model.objects.all()
        return self.main_object_qs

    def get_main_object(self):
        if self.main_object:
            return self.main_object

        queryset = self.get_main_object_qs()
        try:
            pk = self.kwargs.get(self.pk_url_kwarg)
            # Get the single item from the filtered queryset
            self.main_object = queryset.get(pk=pk)
        except queryset.model.DoesNotExist:
            raise Http404(f"No {queryset.model._meta.verbose_name}s "
                          f"found matching the query")
        return self.main_object
