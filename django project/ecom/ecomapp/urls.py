from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
    path('',(views.home)),
    path('about/',(views.about)),
    path('service/',(views.service)),
    path('productdetail/<pid>',(views.productdetail)),
    path('catfilter/<cid>',(views.catfilter)),
    path('sort/<s>',(views.sortbyprice)),
    path('register/',(views.register)),
    path('login/',(views.user_login)),
    path('logout/',(views.user_logout)),
    path('range',(views.pricerange)),
    path('addtocart/<pid>',(views.addtocart)),
    path('viewcart',(views.viewcart)),
    path('remove/<cid>',views.removefromcart),
    path('updateqty/<cid>/<qv>',views.updateqty),
    path('placeorder/',views.placeorder),
    path('pay/',views.makepayment),
    path('senduseremail/',views.senduseremail),
    path('search/', views.search, name='search'),
    # path('viewcart/search/', views.search, name='search'),
    # path('viewcart/search/search', views.search, name='search'),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)