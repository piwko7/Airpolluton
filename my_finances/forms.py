from django import forms
from datetime import date

from my_finances.models import Income, Outcome, Balance

class DateInput(forms.DateInput):
    input_type = 'date'


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['value', 'date', 'type', 'repetitive', 'repetition_interval', 'repetition_time', 'comment']

        # widgets = {
        #     'date': DateInput() # widget to pick date
        # }

    date = forms.DateField(widget=DateInput, initial=date.today())

    def clean(self):
        cleaned_data = self.cleaned_data

        return cleaned_data

    def is_valid(self):
        is_valid = super().is_valid()

        return is_valid

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Do something here
        if commit:
            instance.save()
        return instance

# OUTCOME ----------------------------------------------------

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['value', 'date', 'type', 'repetitive', 'repetition_interval', 'repetition_time', 'comment']

    date = forms.DateField(widget=DateInput, initial=date.today())


# BALANCE ----------------------------------------------------

class BalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['value', 'date', 'type', 'comment']

    date = forms.DateField(widget=DateInput, initial=date.today())

