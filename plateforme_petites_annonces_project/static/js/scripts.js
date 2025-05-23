// Custom JavaScript for Petites Annonces Platform

$(document).ready(function() {
    // Enable tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Enable popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        $('.alert-dismissible').alert('close');
    }, 5000);
    
    // Toggle favorite
    $('.favorite-toggle').on('click', function(e) {
        e.preventDefault();
        const adSlug = $(this).data('ad-slug');
        const favoriteIcon = $(this).find('i');
        
        $.ajax({
            url: `/toggle-favorite/${adSlug}/`,
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            success: function(data) {
                if (data.is_favorite) {
                    favoriteIcon.removeClass('far fa-heart').addClass('fas fa-heart text-danger');
                } else {
                    favoriteIcon.removeClass('fas fa-heart text-danger').addClass('far fa-heart');
                }
            }
        });
    });
    
    // Preview uploaded images before submit
    $('#id_images').on('change', function() {
        const preview = $('#image-preview');
        preview.empty();
        
        if (this.files) {
            Array.from(this.files).forEach(file => {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.append(`
                        <div class="col-md-3 mb-3">
                            <img src="${e.target.result}" class="img-thumbnail" style="height: 150px; object-fit: cover;">
                        </div>
                    `);
                }
                reader.readAsDataURL(file);
            });
        }
    });
    
    // Price range slider
    const priceRange = $('#price-range');
    if (priceRange.length) {
        const minPriceInput = $('#min_price');
        const maxPriceInput = $('#max_price');
        
        priceRange.slider({
            range: true,
            min: 0,
            max: 10000,
            values: [
                parseInt(minPriceInput.val() || 0),
                parseInt(maxPriceInput.val() || 10000)
            ],
            slide: function(event, ui) {
                minPriceInput.val(ui.values[0]);
                maxPriceInput.val(ui.values[1]);
                $('#price-display').text(`${ui.values[0]} € - ${ui.values[1]} €`);
            }
        });
    }
    
    // Search form advanced options toggle
    $('#advanced-search-toggle').on('click', function() {
        $('#advanced-search-options').slideToggle();
        const icon = $(this).find('i');
        if (icon.hasClass('fa-chevron-down')) {
            icon.removeClass('fa-chevron-down').addClass('fa-chevron-up');
            $(this).find('span').text('Masquer les options avancées');
        } else {
            icon.removeClass('fa-chevron-up').addClass('fa-chevron-down');
            $(this).find('span').text('Afficher les options avancées');
        }
    });
    
    // Helper function to get CSRF token
    function getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
    
    // Live search suggestion
    $('#search-input').on('keyup', function() {
        const query = $(this).val();
        if (query.length > 2) {
            $.ajax({
                url: '/search-suggestions/',
                data: { 'q': query },
                success: function(data) {
                    const suggestions = $('#search-suggestions');
                    suggestions.empty();
                    
                    if (data.suggestions.length > 0) {
                        data.suggestions.forEach(suggestion => {
                            suggestions.append(`<a href="/search/?q=${suggestion}" class="list-group-item list-group-item-action">${suggestion}</a>`);
                        });
                        suggestions.show();
                    } else {
                        suggestions.hide();
                    }
                }
            });
        } else {
            $('#search-suggestions').hide();
        }
    });
    
    // Hide suggestions when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.search-container').length) {
            $('#search-suggestions').hide();
        }
    });
    
    // Message character counter
    const messageContent = $('#id_content');
    if (messageContent.length) {
        const counterElement = $('<small class="text-muted ms-2">0/1000 caractères</small>');
        messageContent.after(counterElement);
        
        messageContent.on('input', function() {
            const count = $(this).val().length;
            const remaining = 1000 - count;
            counterElement.text(`${count}/1000 caractères`);
            
            if (remaining < 0) {
                counterElement.removeClass('text-muted').addClass('text-danger');
            } else {
                counterElement.removeClass('text-danger').addClass('text-muted');
            }
        });
    }
}); 