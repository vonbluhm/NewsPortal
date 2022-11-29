from django.urls import path
from django.views.decorators.cache import cache_page
from .views import \
   PostList, PostDetail, PostCreate, PostEdit, PostDelete, PostSearch, UserEdit, upgrade_me, CategoryListView, \
   subscribe


urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='news_list'),
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='news_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('profile/<int:pk>', UserEdit.as_view(), name='user_edit'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe')
]
