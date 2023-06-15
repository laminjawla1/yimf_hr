from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from account import views as account_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("staff.urls")),
    path("payroll/", include("payroll.urls")),
    path("leave_roster/", include("leave_roster.urls")),

    path("profile/", account_views.profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="account/logout.html"), name="logout"),
    path("password_reset/", 
        auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"), name="password_reset"),
    path("password_reset_complete/", 
        auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name="password_reset_complete"),
    path("password_reset_confirm/<uidb64>/<token>", 
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset/done", 
        auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),
    path("password_reset/done", 
        auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Yonna Microfinance - Employee Database"
admin.site.site_title = "Yonna Microfinance HR Admin Portal"
admin.site.index_title = "Welcome To Yonna Microfinance HR Admin Portal"