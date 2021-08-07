class Order(models.Model):
    status = models.CharField( max_length=25, choices=STATUS_CHOICES, default='PENDING')
    total = models.DecimalField( max_digits=22, decimal_places=2)


class Payment(models.Model):
    amount = models.DecimalField( max_digits=22, decimal_places=2)
    order = models.ForeignKey(Order, related_name="payment")


class PaymentInline(admin.TabularInline):
    model = Payment
    formset = PaymentInlineFormset


class PaymentInlineFormset(forms.models.BaseInlineFormSet):
        def clean(self):
            order = None
            valid_forms = 0

            for error in self.errors:
                if error:
                    return

            for cleaned_data in self.cleaned_data:
                amount = cleaned_data.get('amount', 0)
                if order == None:
                    order = cleaned_data.get('order')
                if amount > 0:
                    valid_forms += 1

            if order.status in ['PAID', 'SENT'] and len(valid_forms) > 0:
                raise forms.ValidationError(u'Your error message')