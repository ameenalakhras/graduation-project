from rest_framework import permissions


class OwnerEditOnly(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a UserProfile instance
        return obj.user == request.user


class OwnerDeleteOnly(permissions.BasePermission):
    """
    Object-level permission to only allow the owner to delete the object
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method == "DELETE":
            return obj.user == request.user
        else:
            return True


class OnlyEnrolled(permissions.BasePermission):

    """
    a permission class for the classroom ViewSet
    it makes sure to allow only the user involved in the classroom to request anything from it
    note: the has_object_permission function doesn't work with post requests !
    when any request but post request >> it checks for has_permission then >> checks for has has_object_permission.
    if a post request is sent >> it asks only for has_permission function
    """

    def has_object_permission(self, request, view, obj):
        return (request.user in obj.students.all()) or (request.user == obj.user)


class OnlyTeacherCreates(permissions.BasePermission):
    """
    a permission class for the classroom ViewSet
    it makes sure to allow only the user involved in the classroom to request anything from it
    except the post requests
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a UserProfile instance
        return request.user.groups.filter(name="teachers").exists()
