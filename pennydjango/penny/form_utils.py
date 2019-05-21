from django import forms


class OneLineMultipleChoiceField(forms.MultipleChoiceField):

    def to_one_line(self, value_list):
        return ','.join(value_list)

    def clean(self, value):
        cleaned_list = super().clean(value)
        return self.to_one_line(cleaned_list)
