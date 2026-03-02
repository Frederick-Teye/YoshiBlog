from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def populate_user_avatar(request, user, **kwargs):
    """
    Intercepts the user signup to grab the profile picture URL
    if they signed up via a social provider.
    """
    # The signal passes a 'sociallogin' object if it was a social signup.
    # If they signed up via standard email/password, this will be None.
    sociallogin = kwargs.get("sociallogin")

    if sociallogin:
        provider = sociallogin.account.provider
        extra_data = sociallogin.account.extra_data

        # Google stores the image URL under 'picture'
        if provider == "google":
            avatar_url = extra_data.get("picture")
            if avatar_url:
                user.avatar_url = avatar_url
                user.save()

        # GitHub stores the image URL under 'avatar_url'
        elif provider == "github":
            avatar_url = extra_data.get("avatar_url")
            if avatar_url:
                user.avatar_url = avatar_url
                user.save()
