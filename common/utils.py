class TitleMixin:
    '''Используется для похожих элементов, как правило это title, menu'''
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context