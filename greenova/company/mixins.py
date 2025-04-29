from django.core.exceptions import PermissionDenied


class CompanyAccessMixin:
    """
    Mixin to ensure users can only access data for companies they belong to.

    This mixin assumes that the `request` object has an `active_company` attribute
    set by middleware and that the `active_company` has a `members` relationship.
    """

    def dispatch(self, request, *args, **kwargs):
        company = request.active_company

        if not company:
            raise PermissionDenied("No active company found. Please select a company.")

        if not hasattr(company, 'members') or not company.members.filter(id=request.user.id).exists():
            raise PermissionDenied("You do not have access to this company or the company configuration is invalid.")

        return super().dispatch(request, *args, **kwargs)
