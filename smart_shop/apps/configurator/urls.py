# apps/configurator/urls.py
from django.urls import path

from apps.configurator.views import PublicBuildsView, CloneBuildView, BuildDetailView
from apps.configurator.views.builder import (
    ConfiguratorStartView,
    ComponentCategoryView,
    ComponentSelectionView,
    BuildSummaryView, BuildEditView, AddComponentView, BuildPriceView, RemoveComponentView
)
from apps.configurator.views.feedback import AddCommentView, AddRatingView
from apps.configurator.views.moderation import ModerateCommentsView, ApproveCommentView, DeleteCommentView
from configurator import views
from configurator.views import MyBuildsView, DeleteBuildView, PublishBuildView

app_name = "configurator"

urlpatterns = [
    path("start/", ConfiguratorStartView.as_view(), name="start"),
    path("select-category/", ComponentCategoryView.as_view(), name="select_category"),
    path("select-component/<str:category_slug>/", ComponentSelectionView.as_view(), name="select_component"),
    path("summary/", BuildSummaryView.as_view(), name="summary"),
    path("build/<int:build_id>/edit/", BuildEditView.as_view(), name="edit_build"),
    path("public/", PublicBuildsView.as_view(), name="public_builds"),
    path("clone/<int:build_id>/", CloneBuildView.as_view(), name="clone_build"),
    path("build/<int:build_id>/", BuildDetailView.as_view(), name="build_detail"),
    path("add-component/", AddComponentView.as_view(), name="add_component"),
    path("api/build-price/", BuildPriceView.as_view(), name="build_price"),
    path(
        "remove-component/<int:component_id>/",
        RemoveComponentView.as_view(),
        name="remove_component"
    ),
    path('build/<int:build_id>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('build/<int:build_id>/rate/', AddRatingView.as_view(), name='add_rating'),
    path("moderate/comments/", ModerateCommentsView.as_view(), name="moderate_comments"),
    path("moderate/approve-comment/<int:comment_id>/", ApproveCommentView.as_view(), name="approve_comment"),
    path("moderate/delete-comment/<int:comment_id>/", DeleteCommentView.as_view(), name="delete_comment"),

    path("api/compatibility_status/", views.CompatibilityStatusView.as_view(), name="compatibility_status"),
    path("api/price_update/", views.PriceUpdateView.as_view(), name="price_update"),

    path("my-builds/", MyBuildsView.as_view(), name="my_builds"),
    path("build/delete/<int:build_id>/", DeleteBuildView.as_view(), name="delete_build"),
    path(
        "build/publish/<int:build_id>/",
        PublishBuildView.as_view(),
        name="publish_build"
    ),
]
