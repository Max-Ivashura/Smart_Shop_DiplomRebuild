# apps/configurator/views/public.py
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.configurator.models import PCBuild


# apps/configurator/views/public.py
class BuildDetailView(View):
    """Детальный просмотр сборки."""

    def get(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id, is_public=True)
        return render(request, "configurator/public/build_detail.html", {
            "build": build
        })


class PublicBuildsView(View):
    """Список публичных сборок."""

    def get(self, request):
        public_builds = PCBuild.objects.filter(is_public=True, is_verified=True)
        return render(request, "configurator/public/list.html", {
            "public_builds": public_builds
        })


class CloneBuildView(LoginRequiredMixin, View):
    """Клонирование публичной сборки."""

    def get(self, request, build_id):
        original_build = get_object_or_404(PCBuild, id=build_id, is_public=True)

        # Создаем новую сборку для текущего пользователя
        new_build = PCBuild.objects.create(
            user=request.user,
            total_price=original_build.total_price
        )
        new_build.components.set(original_build.components.all())

        return redirect("configurator:edit_build", build_id=new_build.id)
