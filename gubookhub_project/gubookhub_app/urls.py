from django.urls import path
from gubookhub_app import views

app_name='gubookhub_app'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
	path('profile_page/<username>', views.profile_page, name='profile_page'),
	#path('favourites/', views.favourites, name='favourites'),
	path('search/', views.search, name='search'),
	path('add_book/', views.add_book, name='add_book'),
	path('suggest_courses/', views.CourseListingView.as_view(), name="suggest_courses"),
	path('suggest_subjects/', views.SubjectListingView.as_view(), name="suggest_subjects"),
	path('edit_profile/', views.edit_profile, name='edit_profile'),
	path('items/<slug:subject_name_slug>/', views.subject, name='subject'),
	path('items/<slug:subject_name_slug>/<course_title>/', views.course, name='course'),
	path('favourite_book/', views.FavouriteBookView.as_view(), name='favourite_book'),
	path('subject_more_info/', views.SubjectMoreInfoView.as_view(), name='subject_more_info'),
	#path('<slug:subject_name_slug>/<slug:course_name_slug>/<slug:book_name_slug>/', views.books, name='books'),

]
