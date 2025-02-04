from core.models import ContactInfo, SiteSettings


def get_site_settings(request):
    return {"site_settings": SiteSettings.load()}


def get_contact_info(request):
    return {"contact_info": ContactInfo.load()}
