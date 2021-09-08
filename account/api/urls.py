from django.urls import path

from account.api.views import (
    registration_view,
    ObtainAuthTokenView,
    account_properties_view,
    update_account_view,
    does_account_exist_view,
    user_profile_view,
    ChangePasswordView,
    api_user_follow_view,
    ApiProfileListView,
)

app_name = 'account'

urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('properties', account_properties_view, name="properties"),
    path('properties/update', update_account_view, name="update"),
    path('login', ObtainAuthTokenView.as_view(), name="login"),
    path('register', registration_view, name="register"),
    path('<username>', user_profile_view, name="user"),
    path('<username>/follow', api_user_follow_view, name="follow_action"),
    path('profile_list/', ApiProfileListView.as_view(), name="profile_list"),
]
