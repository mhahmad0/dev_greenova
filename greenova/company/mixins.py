from django.core.exceptions import PermissionDenied


class CompanyAccessMixin:
    """
    Mixin to ensure users can only access data for companies they belong to.
    """

    def dispatch(self, request, *args, **kwargs):
        company = request.active_company

        if not company or not company.members.filter(id=request.user.id).exists():
            raise PermissionDenied("You do not have access to this company.")

        return super().dispatch(request, *args, **kwargs)
