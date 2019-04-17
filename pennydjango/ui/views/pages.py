from django.shortcuts import render

from ui.views.base_views import PublicReactView, BaseView

from rentals.forms import CreateRentPropertyForm


class Home(PublicReactView):
    title = 'Home'
    component = 'pages/home.js'
    template = 'ui/home.html'


class CreateRentProperty(BaseView):
    title = 'Create rental'
    template = 'ui/create_rent_property.html'
    # component = 'pages/base.js'
    # login_required = True

    def get(self, request, *args, **kwargs):
        form = CreateRentPropertyForm()
        context = self.get_context(request, *args, **kwargs)
        return render(request, self.template, {
            **context,
            'form': form,
        })

    # def post(self, request, *args, **kwargs):
    #     form = CreateRentPropertyForm(request.POST)

    #     if form.is_valid():
    #         print("TANK YOU!!!")

    #     return render(request, self.template, {'form': form})
