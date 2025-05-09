from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse

from apps.configurator.models import BuildComment


class ModerateCommentsView(UserPassesTestMixin, View):
    """Панель модерации комментариев"""
    template_name = "configurator/moderation/comments.html"

    def test_func(self):
        return self.request.user.is_staff  # Только для staff

    def get(self, request):
        unapproved_comments = BuildComment.objects.filter(is_approved=False)
        return render(request, self.template_name, {
            "comments": unapproved_comments
        })


class ApproveCommentView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, comment_id):
        comment = BuildComment.objects.get(id=comment_id)
        comment.is_approved = True
        comment.save()
        return redirect(reverse("configurator:moderate_comments"))


class DeleteCommentView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, comment_id):
        BuildComment.objects.get(id=comment_id).delete()
        return redirect(reverse("configurator:moderate_comments"))
