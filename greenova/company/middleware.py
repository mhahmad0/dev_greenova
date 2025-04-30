import logging

from django.utils.deprecation import MiddlewareMixin

from .models import Company

logger = logging.getLogger(__name__)

class ActiveCompanyMiddleware(MiddlewareMixin):
    """
    Middleware to attach the active company to the request object.
    
    If the user is authenticated, it retrieves the active company ID from the session.
    If the company exists, it is attached to the request. Otherwise, it logs an error
    and sets the active company to None. Additionally, it checks if the user is a member
    of the company and handles cases where they are not.
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            active_company_id = request.session.get('active_company_id')
            if active_company_id:
                try:
                    company = Company.objects.get(id=active_company_id)
                    if request.user not in company.users.all():
                        logger.warning(
                            f"User {request.user} is not a member of company {company}."
                        )
                        request.active_company = None
                    else:
                        request.active_company = company
                except Company.DoesNotExist:
                    logger.error(
                        f"Active company with ID {active_company_id} does not exist."
                    )
                    request.active_company = None
            else:
                request.active_company = None
        else:
            request.active_company = None
