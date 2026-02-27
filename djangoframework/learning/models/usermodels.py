# from django.db import models

# """
# Role-Based Access Control (RBAC) with Hierarchical Roles and Permissions

# """
# class Permission(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     class Meta:
#         db_table = 'learning_permission'

# class Role(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
#     permissions = models.ManyToManyField(Permission, related_name='roles')

#     class Meta:
#         db_table = 'learning_role'

# class User(models.Model):
#     username = models.CharField(max_length=100, unique=True)
#     roles = models.ManyToManyField(Role, through='UserRole', related_name='users')

#     class Meta:
#         db_table = 'learning_user'

# class UserRole(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#     assigned_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         db_table = 'learning_user_role'
