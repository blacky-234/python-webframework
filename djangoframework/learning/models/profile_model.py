# from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericRelation


# # Enriched Many-to-Many Relationships

# class Instrument(models.Model):
#     name = models.CharField(max_length=100)
#     symbol = models.CharField(max_length=20,unique=True)

#     class Meta:
#         db_table = 'learning_instrument'

# class Portfolio(models.Model):

#     name = models.CharField(max_length=100)
#     instrument = models.ManyToManyField(Instrument, through='PortfolioInstrument',related_name='portfolios')

#     class Meta:
#         db_table = 'learning_portfolio'

# class PortfolioInstrument(models.Model):
#     portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
#     instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
#     quantity = models.DecimalField(max_digits=20, decimal_places=2)
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'learning_portfolio_instrument'
#         # unique_together = ('portfolio', 'instrument')

# # Self-Referential Foreign Keys for Hierarchical Data

# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     parent = models.ForeignKey(
#         'self',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='children'
#     )

#     def __str__(self):
#         return self.name
    
#     class Meta:
#         db_table = 'learning_category'

# # Generic (Polymorphic) Relationships with Content Types

# class Comment(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'learning_comment'


# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     comments = GenericRelation(Comment)

#     class Meta: 
#         db_table = 'learning_post'


# # Multi-Table Inheritance for Polymorphic Objects

# class Asset(models.Model):
#     name = models.CharField(max_length=100)
#     purchase_date = models.DateField()

# class Machine(Asset):
#     serial_number = models.CharField(max_length=100)

# class Vehicle(Asset):
#     vin_number = models.CharField(max_length=100)


# # Handling Bi-Directional Relationships and Circular Dependencies

# class User(models.Model):
#     mentor = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='mentees')
#     name = models.CharField(max_length=100)