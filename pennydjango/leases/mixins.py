from django.contrib.auth.mixins import AccessMixin


class ClientLeaseAccessMixin(AccessMixin):
    raise_exception = True
    direct = True
    object = None
    object_method = 'get_object'

    def get_my_test_func(self):
        return self.my_test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_my_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def my_test_func(self):
        user = self.request.user
        if not user.is_user_admin and user.is_user_client:
            get_object = getattr(self, self.object_method)
            if get_object:
                test_object = get_object()
                test_object = self.get_lease_member(test_object)
                return user.id == test_object.user_id
            else:
                return self.handle_no_permission()
        return True

    def get_lease_member(self, test_object):
        if not self.direct:
            test_object = test_object.lease_member
        return test_object
