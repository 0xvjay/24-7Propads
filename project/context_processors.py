from core.models import SiteSettings


def get_footer_details(request):
    return {"footer": SiteSettings.load().footer_description}
