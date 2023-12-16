class TitleMixin:
    title = 'CarSell'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.title
        else:
            context['title'] = "CarSell"
        return context
