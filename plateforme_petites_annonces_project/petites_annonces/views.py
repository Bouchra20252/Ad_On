from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from .models import (
    User, UserProfile, Category, Advertisement, AdImage, 
    Message, Conversation, AdComment, SavedSearch, Report, Favorite, Rating
)
from .forms import (
    UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, 
    AdvertisementForm, AdImageFormSet, MessageForm, AdCommentForm, 
    SearchForm, SavedSearchForm, ReportForm
)
from django.contrib.auth import logout

def home(request):
    """Homepage view displaying featured and recent ads"""
    premium_ads = Advertisement.objects.filter(
        status='active', is_premium=True
    ).select_related('category', 'author').order_by('-posted_date')[:6]
    
    recent_ads = Advertisement.objects.filter(
        status='active'
    ).select_related('category', 'author').order_by('-posted_date')[:12]
    
    categories = Category.objects.filter(parent=None).annotate(
        ad_count=Count('advertisements')
    ).order_by('-ad_count')[:8]
    
    search_form = SearchForm()
    
    context = {
        'premium_ads': premium_ads,
        'recent_ads': recent_ads,
        'categories': categories,
        'search_form': search_form,
    }
    return render(request, 'petites_annonces/home.html', context)

class CustomLoginView(LoginView):
    """Custom login view with our form"""
    form_class = UserLoginForm
    template_name = 'petites_annonces/login.html'

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile if it doesn't exist
            UserProfile.objects.get_or_create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé avec succès pour {username}! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'petites_annonces/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view and update"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Votre profil a été mis à jour!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    # Get user's ads, favorites, saved searches
    user_ads = Advertisement.objects.filter(author=request.user).order_by('-posted_date')
    favorites = Favorite.objects.filter(user=request.user).select_related('advertisement')
    saved_searches = SavedSearch.objects.filter(user=request.user)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_ads': user_ads,
        'favorites': favorites,
        'saved_searches': saved_searches
    }
    return render(request, 'petites_annonces/profile.html', context)

class CategoryListView(ListView):
    """View to list all categories"""
    model = Category
    template_name = 'petites_annonces/categories.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(parent=None).annotate(
            ad_count=Count('advertisements')
        ).order_by('name')

class CategoryDetailView(DetailView):
    """View to show a specific category and its ads"""
    model = Category
    template_name = 'petites_annonces/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        # Get all subcategories
        subcategories = Category.objects.filter(parent=category)
        context['subcategories'] = subcategories
        
        # Get all ads in this category and its subcategories
        category_ids = [category.id] + list(subcategories.values_list('id', flat=True))
        ads = Advertisement.objects.filter(
            category_id__in=category_ids, status='active'
        ).select_related('author', 'category').order_by('-is_premium', '-posted_date')
        
        # Apply filters if present
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('q')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            location = form.cleaned_data.get('location')
            
            if query:
                ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
            if min_price:
                ads = ads.filter(price__gte=min_price)
            if max_price:
                ads = ads.filter(price__lte=max_price)
            if location:
                ads = ads.filter(location__icontains=location)
        
        # Pagination
        paginator = Paginator(ads, 16)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['ads'] = page_obj
        context['form'] = form
        return context

@login_required
def advertisement_create(request):
    """View to create a new advertisement"""
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            
            # Process the formset for images
            formset = AdImageFormSet(request.POST, request.FILES, instance=ad)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'Votre annonce a été créée et est en attente de validation!')
                return redirect('ad-detail', slug=ad.slug)
            else:
                # If formset is not valid, delete the ad and show errors
                ad.delete()
        
        # If we get here, form is invalid, recreate formset
        formset = AdImageFormSet(request.POST, request.FILES)
    else:
        form = AdvertisementForm()
        formset = AdImageFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Nouvelle Annonce'
    }
    return render(request, 'petites_annonces/advertisement_form.html', context)

class AdvertisementDetailView(DetailView):
    """View to show a specific advertisement"""
    model = Advertisement
    template_name = 'petites_annonces/advertisement_detail.html'
    context_object_name = 'ad'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view counter if not the author
        if self.request.user != obj.author:
            obj.views += 1
            obj.save(update_fields=['views'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        
        # Get comments
        comments = AdComment.objects.filter(
            advertisement=ad, 
            is_public=True,
            parent=None  # Only get top-level comments
        ).select_related('author').order_by('-created_at')
        
        # Check if user has favorited this ad
        is_favorite = False
        if self.request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(
                user=self.request.user, advertisement=ad
            ).exists()
        
        # Get similar ads (same category, exclude this one)
        similar_ads = Advertisement.objects.filter(
            category=ad.category, status='active'
        ).exclude(id=ad.id).order_by('-posted_date')[:4]
        
        # Add comment form
        comment_form = AdCommentForm()
        
        # Add report form
        report_form = ReportForm()
        
        context.update({
            'comments': comments,
            'is_favorite': is_favorite,
            'similar_ads': similar_ads,
            'comment_form': comment_form,
            'report_form': report_form
        })
        return context

@login_required
def advertisement_update(request, slug):
    """View to update an existing advertisement"""
    ad = get_object_or_404(Advertisement, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            
            # Process the formset for images
            formset = AdImageFormSet(request.POST, request.FILES, instance=ad)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'Votre annonce a été mise à jour!')
                return redirect('ad-detail', slug=ad.slug)
    else:
        form = AdvertisementForm(instance=ad)
        formset = AdImageFormSet(instance=ad)
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Modifier Annonce',
        'ad': ad
    }
    return render(request, 'petites_annonces/advertisement_form.html', context)

@login_required
def advertisement_delete(request, slug):
    """View to delete an advertisement"""
    ad = get_object_or_404(Advertisement, slug=slug, author=request.user)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, f'Votre annonce a été supprimée!')
        return redirect('profile')
    
    return render(request, 'petites_annonces/advertisement_confirm_delete.html', {'ad': ad})

def search_results(request):
    """View to display search results"""
    form = SearchForm(request.GET)
    ads = Advertisement.objects.filter(status='active')
    
    if form.is_valid():
        query = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        
        if query:
            ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category:
            # Get all subcategories too
            category_ids = [category.id] + list(Category.objects.filter(parent=category).values_list('id', flat=True))
            ads = ads.filter(category_id__in=category_ids)
        if min_price:
            ads = ads.filter(price__gte=min_price)
        if max_price:
            ads = ads.filter(price__lte=max_price)
        if location:
            ads = ads.filter(location__icontains=location)
    
    # Sorting
    sort = request.GET.get('sort', 'recent')
    if sort == 'price_low':
        ads = ads.order_by('price')
    elif sort == 'price_high':
        ads = ads.order_by('-price')
    else:  # recent
        ads = ads.order_by('-is_premium', '-posted_date')
    
    # Pagination
    paginator = Paginator(ads.select_related('author', 'category'), 16)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'ads': page_obj,
        'form': form,
        'query': request.GET.get('q', ''),
        'sort': sort,
        'count': ads.count()
    }
    return render(request, 'petites_annonces/search_results.html', context)

@login_required
def save_search(request):
    """View to save a search query"""
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            search.user = request.user
            search.query = request.POST.get('query', '')
            search.save()
            messages.success(request, f'Recherche sauvegardée avec succès!')
            return redirect('profile')
    
    # If not POST or form invalid, redirect back
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_saved_search(request, pk):
    """View to delete a saved search"""
    search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    search.delete()
    messages.success(request, f'Recherche supprimée avec succès!')
    return redirect('profile')

@login_required
def toggle_favorite(request, slug):
    """View to toggle favorite status of an ad"""
    ad = get_object_or_404(Advertisement, slug=slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, advertisement=ad)
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_comment(request, slug):
    """View to add a comment or reply to an advertisement"""
    ad = get_object_or_404(Advertisement, slug=slug)
    
    if request.method == 'POST':
        form = AdCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.advertisement = ad
            comment.author = request.user
            
            # Check if this is a reply to another comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent_comment = get_object_or_404(AdComment, id=parent_id)
                comment.parent = parent_comment
                messages.success(request, f'Votre réponse a été publiée!')
            else:
                messages.success(request, f'Votre question a été publiée!')
                
            comment.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def report_ad(request, slug):
    """View to report an advertisement"""
    ad = get_object_or_404(Advertisement, slug=slug)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.advertisement = ad
            report.save()
            messages.success(request, f'Merci pour votre signalement. Notre équipe va examiner cette annonce.')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def inbox(request):
    """View to display user's inbox"""
    # Get all conversations for this user
    conversations = Conversation.objects.filter(
        participants=request.user
    ).order_by('-updated_at')
    
    context = {
        'conversations': conversations
    }
    return render(request, 'petites_annonces/inbox.html', context)

@login_required
def conversation_detail(request, pk):
    """View to display a conversation and its messages"""
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    messages_list = Message.objects.filter(
        conversation=conversation
    ).order_by('timestamp')
    
    # Mark messages as read
    messages_list.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    # Get the other participant
    other_user = conversation.participants.exclude(id=request.user.id).first()
    
    # Handle new message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.conversation = conversation
            
            # Set subject based on first message if available
            if messages_list.exists() and not msg.subject:
                first_message = messages_list.first()
                msg.subject = first_message.subject
            elif conversation.advertisement and not msg.subject:
                msg.subject = f"À propos de: {conversation.advertisement.title}"
                
            msg.save()
            
            # Update conversation timestamp
            conversation.save()  # This updates the updated_at field
            
            return redirect('conversation-detail', pk=pk)
    else:
        form = MessageForm()
    
    context = {
        'conversation': conversation,
        'messages': messages_list,
        'other_user': other_user,
        'form': form
    }
    return render(request, 'petites_annonces/conversation_detail.html', context)

@login_required
def new_message(request, user_id, ad_slug=None):
    """View to start a new conversation"""
    receiver = get_object_or_404(User, id=user_id)
    ad = None
    
    if ad_slug:
        ad = get_object_or_404(Advertisement, slug=ad_slug)
    
    # Check if conversation already exists
    conversations = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=receiver
    )
    
    if ad:
        conversations = conversations.filter(advertisement=ad)
    
    if conversations.exists():
        # Conversation exists, redirect to it
        return redirect('conversation-detail', pk=conversations.first().id)
    
    # Handle new conversation
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Create new conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, receiver)
            if ad:
                conversation.advertisement = ad
                conversation.save()
            
            # Create message
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = receiver
            msg.conversation = conversation
            if ad:
                msg.advertisement = ad
                if not msg.subject:
                    msg.subject = f"À propos de: {ad.title}"
            msg.save()
            
            return redirect('conversation-detail', pk=conversation.id)
    else:
        initial = {}
        if ad:
            initial['subject'] = f"À propos de: {ad.title}"
        form = MessageForm(initial=initial)
    
    context = {
        'form': form,
        'receiver': receiver,
        'ad': ad
    }
    return render(request, 'petites_annonces/new_message.html', context)

# Admin views
@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les permissions requises.")
        return redirect('home')
    
    # Get pending ads
    pending_ads = Advertisement.objects.filter(status='pending').order_by('-posted_date')
    
    # Get reports
    reports = Report.objects.filter(is_reviewed=False).order_by('-timestamp')
    
    # Get stats
    total_users = User.objects.count()
    total_ads = Advertisement.objects.count()
    active_ads = Advertisement.objects.filter(status='active').count()
    
    context = {
        'pending_ads': pending_ads,
        'reports': reports,
        'total_users': total_users,
        'total_ads': total_ads,
        'active_ads': active_ads
    }
    return render(request, 'petites_annonces/admin_dashboard.html', context)

@login_required
def moderate_ad(request, pk, action):
    """View to moderate an advertisement"""
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les permissions requises.")
        return redirect('home')
    
    ad = get_object_or_404(Advertisement, pk=pk)
    
    if action == 'approve':
        ad.status = 'active'
        ad.save()
        messages.success(request, f'Annonce "{ad.title}" approuvée.')
    elif action == 'reject':
        ad.status = 'flagged'
        ad.save()
        messages.success(request, f'Annonce "{ad.title}" rejetée.')
    
    return redirect('admin-dashboard')

def user_ads(request, username):
    """View to display ads from a specific user"""
    user = get_object_or_404(User, username=username)
    ads = Advertisement.objects.filter(author=user, status='active').order_by('-posted_date')
    
    # Pagination
    paginator = Paginator(ads, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'ads': page_obj,
        'profile_user': user,
        'ad_count': ads.count(),
    }
    return render(request, 'petites_annonces/user_ads.html', context)

def moderate_report(request, pk):
    """View to moderate a report"""
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les permissions requises.")
        return redirect('home')
    
    report = get_object_or_404(Report, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'ignore':
            report.is_reviewed = True
            report.reviewed_by = request.user
            report.save()
            messages.success(request, f'Le signalement a été ignoré.')
        elif action == 'flag':
            ad = report.advertisement
            ad.status = 'flagged'
            ad.save()
            
            report.is_reviewed = True
            report.reviewed_by = request.user
            report.save()
            messages.success(request, f'L\'annonce a été signalée.')
        elif action == 'delete':
            ad = report.advertisement
            ad.delete()
            messages.success(request, f'L\'annonce a été supprimée.')
    
    return redirect('admin-dashboard')

def custom_logout(request):
    """Custom logout view that accepts GET requests"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès!')
    return redirect('home')
