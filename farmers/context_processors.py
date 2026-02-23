def farmer_context(request):
    """Add farmer-related context to all templates"""
    context = {}
    
    if request.user.is_authenticated and request.user.is_farmer:
        try:
            profile = request.user.farmer_profile
            context['farmer_profile'] = profile
            context['farmer_credit_score'] = profile.credit_score
            context['farmer_credit_limit'] = profile.credit_limit
        except:
            context['farmer_profile'] = None
            context['farmer_credit_score'] = 0
            context['farmer_credit_limit'] = 0
    
    return context
