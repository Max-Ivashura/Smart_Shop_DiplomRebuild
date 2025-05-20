# apps/configurator/views/public.py
from django.contrib import messages
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.configurator.models import PCBuild
from apps.configurator.models import BuildComponent
from apps.configurator.models import BuildRating


class DeleteBuildView(LoginRequiredMixin, View):
    def post(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)
        build.delete()
        messages.success(request, "Сборка удалена.")
        return redirect("configurator:my_builds")


class MyBuildsView(LoginRequiredMixin, View):
    """Список сохранённых сборок пользователя."""
    template_name = "configurator/public/my_builds.html"

    def get(self, request):
        builds = PCBuild.objects.filter(user=request.user)
        return render(request, self.template_name, {"builds": builds})


class PublishBuildView(LoginRequiredMixin, View):
    def post(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)
        build.is_public = True
        build.is_verified = True  # Автоматическая проверка
        build.save()
        messages.success(request, "Сборка успешно опубликована!")
        return redirect("configurator:my_builds")


# apps/configurator/views/public.py
class BuildDetailView(View):
    """Детальный просмотр сборки."""

    def get(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id, is_public=True)
        user_rating = None

        if request.user.is_authenticated:
            try:
                user_rating = BuildRating.objects.get(
                    build=build,
                    user=request.user
                ).value
            except BuildRating.DoesNotExist:
                pass

        return render(request, "configurator/public/build_detail.html", {
            "build": build,
            "user_rating": user_rating  # Добавляем в контекст
        })


class PublicBuildsView(View):
    """Список публичных сборок."""

    def get(self, request):
        public_builds = PCBuild.objects.filter(is_public=True, is_verified=True)
        return render(request, "configurator/public/list.html", {
            "public_builds": public_builds
        })


class CloneBuildView(LoginRequiredMixin, View):
    def get(self, request, build_id):
        original_build = get_object_or_404(PCBuild, id=build_id, is_public=True)

        # Создаем новую сборку с теми же данными, кроме полей, связанных с публикацией
        new_build = PCBuild.objects.create(
            user=request.user,
            is_public=False,
            is_verified=False,
            total_price=original_build.total_price,
            compatibility_errors={}  # Очищаем ошибки, так как они пересчитаются
        )

        # Копируем BuildComponent с сохранением quantity
        for component in original_build.buildcomponent_set.all():
            BuildComponent.objects.create(
                build=new_build,
                product=component.product,
                quantity=component.quantity
            )

        # Пересчитываем цену и проверяем совместимость
        new_build.update_total_price()
        new_build.check_compatibility()

        return redirect("configurator:edit_build", build_id=new_build.id)
