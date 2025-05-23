from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def exclude_user(queryset, user):
    """Filter to exclude the current user from a queryset"""
    return queryset.exclude(id=user.id)

@register.filter
def unread_messages_count(conversation, user):
    """Count unread messages for a conversation"""
    return conversation.messages.filter(receiver=user, is_read=False).count() 