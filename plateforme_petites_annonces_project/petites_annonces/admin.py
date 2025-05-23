from django.contrib import admin
from .models import (
    UserProfile, Category, Advertisement, AdImage, Message, 
    Conversation, AdComment, SavedSearch, Report, Favorite, Rating
)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'reputation_score')
    search_fields = ('user__username', 'user__email', 'city')
    list_filter = ('city',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('parent',)

class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 1

class AdCommentInline(admin.TabularInline):
    model = AdComment
    extra = 0

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'author', 'status', 'posted_date', 'is_premium')
    list_filter = ('status', 'category', 'is_premium', 'posted_date')
    search_fields = ('title', 'description', 'author__username', 'location')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'posted_date'
    readonly_fields = ('views',)
    inlines = [AdImageInline, AdCommentInline]

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('subject', 'content', 'sender__username', 'receiver__username')
    date_hierarchy = 'timestamp'

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'updated_at')
    filter_horizontal = ('participants',)
    search_fields = ('participants__username', 'advertisement__title')
    date_hierarchy = 'created_at'

class AdCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'advertisement', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('content', 'author__username', 'advertisement__title')
    date_hierarchy = 'created_at'

class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'category', 'created_at', 'send_notifications')
    list_filter = ('category', 'send_notifications')
    search_fields = ('name', 'query', 'user__username')
    date_hierarchy = 'created_at'

class ReportAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'reporter', 'report_type', 'timestamp', 'is_reviewed')
    list_filter = ('report_type', 'is_reviewed')
    search_fields = ('details', 'reporter__username', 'advertisement__title')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'advertisement', 'added_date')
    list_filter = ('added_date',)
    search_fields = ('user__username', 'advertisement__title')
    date_hierarchy = 'added_date'

class RatingAdmin(admin.ModelAdmin):
    list_display = ('rater', 'rated_user', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('rater__username', 'rated_user__username', 'comment')
    date_hierarchy = 'created_at'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(AdComment, AdCommentAdmin)
admin.site.register(SavedSearch, SavedSearchAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Rating, RatingAdmin)
