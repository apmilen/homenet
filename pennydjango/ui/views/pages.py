from ui.views.base_views import PublicReactView


class Home(PublicReactView):
    title = 'Home'
    component = 'pages/home.js'
    template = 'ui/home.html'
