from django.views.generic.edit import FormMixin
 
 
class MultipleFormsMixin(FormMixin):
    """
    A mixin that provides a way to show and handle several forms in a
    request.
    """
    form_classes = {} # set the form classes as a mapping
 
    def get_form_classes(self):
        return self.form_classes
 
    def get_forms(self, form_classes):
        return dict([(key, klass(**self.get_form_kwargs())) \
            for key, klass in form_classes.items()])
 
    def forms_valid(self, forms):
        return super(MultipleFormsMixin, self).form_valid(forms)
 
    def forms_invalid(self, forms):
        return self.render_to_response(self.get_context_data(forms=forms))
