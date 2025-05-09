from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.configurator.models import PCBuild, BuildComment, BuildRating


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id)
        text = request.POST.get('text', '').strip()

        if text:
            BuildComment.objects.create(
                build=build,
                user=request.user,
                text=text
            )
            messages.success(request, "Комментарий отправлен на модерацию!")
        else:
            messages.error(request, "Комментарий не может быть пустым.")

        return redirect("configurator:build_detail", build_id=build_id)


class AddRatingView(LoginRequiredMixin, View):
    def post(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id)
        rating_value = int(request.POST.get('rating', 0))

        if 1 <= rating_value <= 5:
            BuildRating.objects.update_or_create(
                build=build,
                user=request.user,
                defaults={'value': rating_value}
            )
            messages.success(request, "Спасибо за оценку!")
        else:
            messages.error(request, "Некорректная оценка.")

        return redirect("configurator:build_detail", build_id=build_id)