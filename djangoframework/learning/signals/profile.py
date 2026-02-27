# #Automatically Creating Portfolio Summary on Association

# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver

# from learning.profile_model import Portfolio

# @receiver(m2m_changed, sender=Portfolio.instruments.through)
# def update_portfolio_summary(sender, instance, action, **kwargs):
#     if action in ['post_add', 'post_remove', 'post_clear']:
#         instance.update_summary()  # Custom method on Portfolio to refresh data