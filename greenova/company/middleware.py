from django.utils.deprecation import MiddlewareMixin

from .models import Company


class ActiveCompanyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            active_company_id = request.session.get('active_company_id')
            if active_company_id:
                try:
                    request.active_company = Company.objects.get(id=active_company_id)
                except Company.DoesNotExist:
                    request.active_company = None
            else:
                request.active_company = None
        else:
            request.active_company = None
