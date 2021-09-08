from django.urls import path
from account.views import (
    profile_view,
    account_view
)

app_name = 'account'

urlpatterns = [
    path('<username>/', profile_view, name="profile"),
    path('account/', account_view, name='account'),
]
