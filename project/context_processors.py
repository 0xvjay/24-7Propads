from core.models import SiteSettings


def get_site_settings(request):
    return {"site_settings": SiteSettings.load()}
