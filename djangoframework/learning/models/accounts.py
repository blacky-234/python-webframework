# from django.db import models
# from django.core.exceptions import ValidationError
# from django.db.models import Q, F, Sum, Count, Avg, Max, Min
# from django.db.models.constraints import UniqueConstraint, CheckConstraint
# from django.utils import timezone


# # Abstract Base Classes and Multi-Table Inheritance

# class TimestampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# class Transaction(TimestampedModel):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20)
#     description = models.TextField()
#     confirmed = models.BooleanField(default=False)


#     """
#     Data Integrity and Validation Beyond Field Constraints
#     Overriding Model clean() Method
#     """
#     def clean(self):
#         if self.amount <= 0:
#             raise ValidationError('Amount must be positive.')
#         if self.status not in ['pending', 'success', 'failed']:
#             raise ValidationError('Invalid status.')

#     class Meta:
#         db_table = 'learning_transaction'
#         constraints = [
#             CheckConstraint(check=Q(amount__gt=0), name='positive_amount'),
#             CheckConstraint(check=Q(confirmed=True) | Q(amount=F('amount')), name='confirmed_logic'),
#         ]




# class Payment(TimestampedModel):
#     reference_number = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'learning_payment'

# class CreditCardPayment(Payment):
#     card_number = models.CharField(max_length=16)

#     class Meta:
#         db_table = 'learning_credit_card_payment'

# # Proxy Models for Behavior Customization

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=8, decimal_places=2)

#     class Meta:
#         db_table = 'learning_product'

# class DiscountedProduct(Product):
#     class Meta:
#         proxy = True

#     def discounted_price(self, discount_percentage):
#         return self.price * (1 - discount_percentage / 100)

# # soft delete implementation

# class SoftDeleteModel(models.Model):
#     is_deleted = models.BooleanField(default=False)
#     deleted_at = models.DateTimeField(null=True, blank=True)

#     def delete(self):
#         self.is_deleted = True
#         self.deleted_at = timezone.now()
#         self.save()

#     class Meta:
#         abstract = True

# # creating a model that inherits from SoftDeleteModel

# class SoftCreatedModel(models.Model):
#     is_created = models.BooleanField(default=False)
#     created_at = models.DateTimeField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if not self.is_created:
#             self.is_created = True
#             self.created_at = timezone.now()
#         super().save(*args, **kwargs)

#     class Meta:
#         abstract = True