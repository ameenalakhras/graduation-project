from django.shortcuts import render

# Create your views here.


def signup():
    pass


@require_http_methods(["POST"])
def log_out(request):
    """
    logs out the user and removes it's session
    """
    logout(request)
    return HttpResponseRedirect('/')

@login_required
@require_http_methods(["POST"])
def update_password(request):
    """update the user password given the old and the new passwords"""
    current_password = request.POST.get('currentPassword', '')
    new_password = request.POST.get('newPassword', '')
    new_password_confirmation = request.POST.get('confirmNewPassword', '')
    user = authenticate(username=request.user.username, password=current_password)

    if user is not None:
        if new_password == new_password_confirmation:
            request.user.set_password(new_password)
            request.user.save()
            message = "Password has been reset."
            status = True
        else:
            message = "new password and new password confirmation differ."
            status = False
    else:
        message = "old password is not right, please try again."
        status = False

    response = JsonResponse({
        "answer": {
            "message": message,
            "status": status
        },
    })
    return response
