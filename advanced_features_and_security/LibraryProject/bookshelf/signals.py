from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Book


# Permissions & Groups guide
# --------------------------
# 1) Permissions are defined on the Book model via Book.Meta.permissions:
#      can_view, can_create, can_edit, can_delete
#
# 2) This module automatically creates Groups and assigns those permissions
#    after migrations (post_migrate), so they appear in the Django admin.
#
#    Groups created:
#      - Viewers: can_view
#      - Editors: can_view, can_create, can_edit
#      - Admins:  can_view, can_create, can_edit, can_delete
#
# 3) Usage examples in code:
#      @permission_required('bookshelf.can_edit')
#      request.user.has_perm('bookshelf.can_delete')
#
# Notes:
# - We use .permissions.add(...) instead of .set(...) so any extra permissions
#   you assign manually in the Django admin are preserved.


@receiver(post_migrate)
def ensure_groups_and_permissions(sender, **kwargs):
    """Create default groups and assign custom Book permissions.

    Runs after migrations so Permission rows exist.
    Safe to run multiple times.
    """
    # Only run when the bookshelf app has migrated
    if getattr(sender, "name", None) != "bookshelf":
        return

    content_type = ContentType.objects.get_for_model(Book)

    perm_codenames = {
        "can_view": "Can view book",
        "can_create": "Can create book",
        "can_edit": "Can edit book",
        "can_delete": "Can delete book",
    }

    permissions = {}
    for codename in perm_codenames:
        permissions[codename] = Permission.objects.get(
            content_type=content_type,
            codename=codename,
        )

    viewers, _ = Group.objects.get_or_create(name="Viewers")
    editors, _ = Group.objects.get_or_create(name="Editors")
    admins, _ = Group.objects.get_or_create(name="Admins")

    viewers.permissions.add(
        permissions["can_view"],
    )

    editors.permissions.add(
        permissions["can_view"],
        permissions["can_create"],
        permissions["can_edit"],
    )

    admins.permissions.add(
        permissions["can_view"],
        permissions["can_create"],
        permissions["can_edit"],
        permissions["can_delete"],
    )
