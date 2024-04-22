class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldn in self.visible_fields():
            fieldn.field.widget.attrs["class"] = "form-control"
