from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.paginator import Paginator

from .models import Company, CompanyMembership, CompanyDocument
from .forms import (
    CompanyForm, CompanyMembershipForm, CompanyDocumentForm,
    CompanySearchForm, AddUserToCompanyForm
)

import logging

logger = logging.getLogger(__name__)


def is_company_admin(user):
    """Check if user is a company admin or superuser."""
    if not user.is_authenticated:
        return False

    # Superusers can manage all companies
    if user.is_superuser:
        return True

    # Check if user is an admin in any company
    return CompanyMembership.objects.filter(
        user=user,
        role__in=['owner', 'admin']
    ).exists()


@login_required
def company_list(request):
    """View for listing companies."""
    search_form = CompanySearchForm(request.GET)
    companies_query = Company.objects.all()

    # Apply filters if form is submitted
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        company_type = search_form.cleaned_data.get('company_type')
        industry = search_form.cleaned_data.get('industry')
        is_active = search_form.cleaned_data.get('is_active')

        if search:
            companies_query = companies_query.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        if company_type:
            companies_query = companies_query.filter(company_type=company_type)

        if industry:
            companies_query = companies_query.filter(industry=industry)

        if is_active is not None:
            companies_query = companies_query.filter(is_active=is_active)

    # Add member count annotation
    companies_query = companies_query.annotate(member_count=Count('members'))

    # Handle pagination
    paginator = Paginator(companies_query, 10)
    page_number = request.GET.get('page', 1)
    companies = paginator.get_page(page_number)

    # Check user permissions for each company
    user_permissions = {}
    if not request.user.is_superuser:
        for company in companies:
            try:
                membership = CompanyMembership.objects.get(
                    company=company,
                    user=request.user
                )
                user_permissions[company.id] = membership.role
            except CompanyMembership.DoesNotExist:
                user_permissions[company.id] = None

    context = {
        'companies': companies,
        'search_form': search_form,
        'user_permissions': user_permissions,
        'page_obj': companies,
        'can_create': is_company_admin(request.user),
    }

    if request.htmx:
        return render(request, 'company/partials/company_list.html', context)
    return render(request, 'company/company_list.html', context)


@login_required
def company_detail(request, company_id):
    """View for viewing company details."""
    company = get_object_or_404(Company, id=company_id)

    # Get projects related to this company
    projects = company.projects.all()

    # Get members with their roles
    members = CompanyMembership.objects.filter(company=company).select_related('user')

    # Get documents
    documents = company.documents.all()

    # Check user permissions
    can_edit = False
    can_manage_members = False
    if request.user.is_superuser:
        can_edit = True
        can_manage_members = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role in ['owner', 'admin']:
                can_edit = True
                can_manage_members = True
            elif membership.role == 'manager':
                can_manage_members = True
        except CompanyMembership.DoesNotExist:
            pass

    context = {
        'company': company,
        'projects': projects,
        'members': members,
        'documents': documents,
        'can_edit': can_edit,
        'can_manage_members': can_manage_members,
    }

    if request.htmx:
        return render(request, 'company/partials/company_detail.html', context)
    return render(request, 'company/company_detail.html', context)


@login_required
@user_passes_test(is_company_admin)
def company_create(request):
    """View for creating a new company."""
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()

            # Add the creator as an owner of the company
            CompanyMembership.objects.create(
                company=company,
                user=request.user,
                role='owner',
                is_primary=True
            )

            messages.success(request, f"Company '{company.name}' created successfully!")

            if request.htmx:
                return HttpResponse(
                    status=200,
                    headers={
                        'HX-Redirect': reverse('company:detail', args=[company.id])
                    }
                )
            return redirect('company:detail', company_id=company.id)
    else:
        form = CompanyForm()

    context = {'form': form, 'action': 'Create'}

    if request.htmx:
        return render(request, 'company/partials/company_form.html', context)
    return render(request, 'company/company_form.html', context)


@login_required
def company_edit(request, company_id):
    """View for editing a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check if user has permission to edit this company
    if not request.user.is_superuser:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role not in ['owner', 'admin']:
                messages.error(request, "You don't have permission to edit this company.")
                return redirect('company:detail', company_id=company.id)
        except CompanyMembership.DoesNotExist:
            messages.error(request, "You don't have permission to edit this company.")
            return redirect('company:detail', company_id=company.id)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save()
            messages.success(request, f"Company '{company.name}' updated successfully!")

            if request.htmx:
                return HttpResponse(
                    status=200,
                    headers={
                        'HX-Redirect': reverse('company:detail', args=[company.id])
                    }
                )
            return redirect('company:detail', company_id=company.id)
    else:
        form = CompanyForm(instance=company)

    context = {'form': form, 'company': company, 'action': 'Update'}

    if request.htmx:
        return render(request, 'company/partials/company_form.html', context)
    return render(request, 'company/company_form.html', context)


@login_required
@user_passes_test(is_company_admin)
def company_delete(request, company_id):
    """View for deleting a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check if user has permission to delete this company
    if not request.user.is_superuser:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user,
                role='owner'
            )
        except CompanyMembership.DoesNotExist:
            messages.error(request, "Only the owner can delete this company.")
            return redirect('company:detail', company_id=company.id)

    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f"Company '{company_name}' deleted successfully!")

        if request.htmx:
            return HttpResponse(
                status=200,
                headers={'HX-Redirect': reverse('company:list')}
            )
        return redirect('company:list')

    context = {'company': company}

    if request.htmx:
        return render(request, 'company/partials/company_delete_confirm.html', context)
    return render(request, 'company/company_delete.html', context)


@login_required
def manage_members(request, company_id):
    """View for managing company members."""
    company = get_object_or_404(Company, id=company_id)

    # Check if user has permission to manage members
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role in ['owner', 'admin', 'manager']:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        messages.error(request, "You don't have permission to manage members.")
        return redirect('company:detail', company_id=company.id)

    # Get all members
    members = CompanyMembership.objects.filter(company=company).select_related('user')

    # Initialize forms
    add_user_form = AddUserToCompanyForm()

    context = {
        'company': company,
        'members': members,
        'add_user_form': add_user_form,
        'can_edit': can_manage,
    }

    if request.htmx:
        return render(request, 'company/partials/company_members.html', context)
    return render(request, 'company/company_members.html', context)


@login_required
@require_http_methods(["POST"])
def add_member(request, company_id):
    """View for adding a member to a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check permissions
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role in ['owner', 'admin', 'manager']:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    # Process form
    form = AddUserToCompanyForm(request.POST)
    if form.is_valid():
        user = form.cleaned_data['user']
        role = form.cleaned_data['role']
        department = form.cleaned_data['department']
        position = form.cleaned_data['position']
        is_primary = form.cleaned_data['is_primary']

        # Check if user is already a member
        if CompanyMembership.objects.filter(company=company, user=user).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'User is already a member of this company'
            }, status=400)

        # Create membership
        membership = CompanyMembership.objects.create(
            company=company,
            user=user,
            role=role,
            department=department,
            position=position,
            is_primary=is_primary
        )

        # Return updated member list
        members = CompanyMembership.objects.filter(company=company).select_related('user')
        html = render_to_string('company/partials/member_list.html', {
            'members': members,
            'company': company,
            'can_edit': can_manage
        }, request=request)

        return HttpResponse(html)

    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@require_http_methods(["POST"])
def remove_member(request, company_id, member_id):
    """View for removing a member from a company."""
    company = get_object_or_404(Company, id=company_id)
    membership = get_object_or_404(CompanyMembership, id=member_id, company=company)

    # Check permissions
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            user_membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            # Only owner and admin can remove members
            if user_membership.role in ['owner', 'admin']:
                can_manage = True
            # Managers can only remove regular members
            elif user_membership.role == 'manager' and membership.role not in ['owner', 'admin', 'manager']:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    # Can't remove the owner
    if membership.role == 'owner' and not request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'message': 'Company owner cannot be removed'
        }, status=400)

    # Remove membership
    membership.delete()

    # Return updated member list
    members = CompanyMembership.objects.filter(company=company).select_related('user')
    html = render_to_string('company/partials/member_list.html', {
        'members': members,
        'company': company,
        'can_edit': can_manage
    }, request=request)

    return HttpResponse(html)


@login_required
def update_member_role(request, company_id, member_id):
    """View for updating a member's role in a company."""
    company = get_object_or_404(Company, id=company_id)
    membership = get_object_or_404(CompanyMembership, id=member_id, company=company)

    # Check permissions
    can_manage = False
    if request.user.is_superuser:
        can_manage = True
    else:
        try:
            user_membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            # Only owner and admin can update roles
            if user_membership.role in ['owner', 'admin']:
                can_manage = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_manage:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    if request.method == 'POST':
        form = CompanyMembershipForm(request.POST, instance=membership)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = CompanyMembershipForm(instance=membership)

    context = {
        'form': form,
        'membership': membership,
        'company': company
    }

    return render(request, 'company/partials/member_role_form.html', context)


@login_required
def upload_document(request, company_id):
    """View for uploading a document to a company."""
    company = get_object_or_404(Company, id=company_id)

    # Check permissions
    can_edit = False
    if request.user.is_superuser:
        can_edit = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role in ['owner', 'admin', 'manager']:
                can_edit = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_edit:
        messages.error(request, "You don't have permission to upload documents.")
        return redirect('company:detail', company_id=company.id)

    if request.method == 'POST':
        form = CompanyDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.company = company
            document.uploaded_by = request.user
            document.save()

            messages.success(request, f"Document '{document.name}' uploaded successfully!")

            if request.htmx:
                documents = company.documents.all()
                html = render_to_string('company/partials/document_list.html', {
                    'documents': documents,
                    'company': company,
                    'can_edit': can_edit
                }, request=request)
                return HttpResponse(html)
            return redirect('company:detail', company_id=company.id)
    else:
        form = CompanyDocumentForm()

    context = {
        'form': form,
        'company': company,
    }

    if request.htmx:
        return render(request, 'company/partials/document_form.html', context)
    return render(request, 'company/document_form.html', context)


@login_required
def delete_document(request, company_id, document_id):
    """View for deleting a document from a company."""
    company = get_object_or_404(Company, id=company_id)
    document = get_object_or_404(CompanyDocument, id=document_id, company=company)

    # Check permissions
    can_edit = False
    if request.user.is_superuser:
        can_edit = True
    else:
        try:
            membership = CompanyMembership.objects.get(
                company=company,
                user=request.user
            )
            if membership.role in ['owner', 'admin']:
                can_edit = True
            elif membership.role == 'manager' and document.uploaded_by == request.user:
                can_edit = True
        except CompanyMembership.DoesNotExist:
            pass

    if not can_edit:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    if request.method == 'POST':
        document.delete()
        messages.success(request, f"Document '{document.name}' deleted successfully!")

        if request.htmx:
            documents = company.documents.all()
            html = render_to_string('company/partials/document_list.html', {
                'documents': documents,
                'company': company,
                'can_edit': can_edit
            }, request=request)
            return HttpResponse(html)
        return redirect('company:detail', company_id=company.id)

    context = {
        'document': document,
        'company': company,
    }

    if request.htmx:
        return render(request, 'company/partials/document_delete_confirm.html', context)
    return render(request, 'company/document_delete.html', context)
