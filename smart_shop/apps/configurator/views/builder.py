# apps/configurator/views/builder.py
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.products.models import Category, Product
from apps.configurator.models import PCBuild
from apps.configurator.utils.compatibility import CompatibilityChecker
from apps.cart.models import Cart, CartItem
from apps.configurator.models import BuildComponent


class RemoveComponentView(LoginRequiredMixin, View):
    def post(self, request, component_id):
        build_id = request.session.get("current_build_id")
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)

        component = get_object_or_404(BuildComponent, id=component_id, build=build)
        component.delete()

        build.update_total_price()
        build.check_compatibility()

        return redirect("configurator:edit_build", build_id=build.id)


class BuildPriceView(LoginRequiredMixin, View):
    def get(self, request):
        build_id = request.session.get("current_build_id")
        if not build_id:
            return JsonResponse({"total_price": 0})

        build = get_object_or_404(PCBuild, id=build_id)
        total = sum(product.price for product in build.components.all())
        return JsonResponse({"total_price": total})


# apps/configurator/views/builder.py
class AddComponentView(LoginRequiredMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        build_id = request.session.get("current_build_id")
        if not build_id:
            # Создаем сборку только при добавлении первого компонента
            build = PCBuild.objects.create(user=request.user)
            request.session["current_build_id"] = build.id
        else:
            build = get_object_or_404(PCBuild, id=build_id)

        # Удаляем компоненты той же категории
        BuildComponent.objects.filter(
            build=build,
            product__category=product.category
        ).delete()

        # Добавляем новый компонент
        BuildComponent.objects.create(
            build=build,
            product=product,
            quantity=1
        )

        build.update_total_price()
        build.check_compatibility()

        return redirect("configurator:select_category")


# apps/configurator/views/builder.py
class ConfiguratorStartView(LoginRequiredMixin, View):
    """Создает новую сборку и перенаправляет на выбор категории."""

    def get(self, request):
        # Удаляем старую незавершенную сборку
        if "current_build_id" in request.session:
            build_id = request.session["current_build_id"]
            PCBuild.objects.filter(id=build_id, components__isnull=True).delete()
            del request.session["current_build_id"]

        # Создаем новую сборку
        build = PCBuild.objects.create(user=request.user)
        request.session["current_build_id"] = build.id
        return redirect("configurator:select_category")


# apps/configurator/views/builder.py
class ComponentCategoryView(LoginRequiredMixin, View):
    """Выбор категории компонента с визуализацией конфликтов"""

    REQUIRED_SLUGS = [
        'processor', 'motherboard', 'ram', 'psu', 'case'
    ]

    CPU_COOLING_SLUGS = ['cooler', 'watercooling']

    STORAGE_SLUGS = ['ssd', 'm2ssd', 'hdd']

    OPTIONAL_SLUGS = [
        'videocard', 'thermalpaste', 'fan'
    ]

    def get(self, request):
        build_id = request.session.get('current_build_id')
        if not build_id:
            return redirect('configurator:start')

        try:
            build = PCBuild.objects.get(id=build_id)
        except PCBuild.DoesNotExist:
            # Если сборка удалена, очищаем сессию
            del request.session["current_build_id"]
            return redirect("configurator:start")

        build = PCBuild.objects.get(id=build_id)
        selected_components = build.buildcomponent_set.select_related('product').all()

        # Проверка совместимости
        checker = CompatibilityChecker([bc.product for bc in selected_components])
        compatibility_errors = checker.validate()

        # Формирование данных категорий
        selected_slugs = []
        total_conflicts = 0

        required_categories = []
        cpu_cooling_categories = []
        storage_categories = []
        optional_categories = []

        for category in Category.objects.filter(
                slug__in=self.REQUIRED_SLUGS + self.CPU_COOLING_SLUGS + self.STORAGE_SLUGS + self.OPTIONAL_SLUGS):
            component = selected_components.filter(product__category=category).first()
            has_conflict = any(
                error_key in compatibility_errors
                and error_key == category.slug[:-1]
                for error_key in compatibility_errors
            )

            if has_conflict:
                total_conflicts += 1

            if category.slug in self.REQUIRED_SLUGS:
                required_categories.append({
                    'slug': category.slug,
                    'name': category.name,
                    'image': category.image,
                    'has_conflict': has_conflict,
                    'is_selected': component is not None
                })
            elif category.slug in self.CPU_COOLING_SLUGS:
                cpu_cooling_categories.append({
                    'slug': category.slug,
                    'name': category.name,
                    'image': category.image,
                    'has_conflict': has_conflict,
                    'is_selected': component is not None
                })
            elif category.slug in self.STORAGE_SLUGS:
                storage_categories.append({
                'slug': category.slug,
                'name': category.name,
                'image': category.image,
                'has_conflict': has_conflict,
                'is_selected': component is not None
                })
            else:
                optional_categories.append({
                    'slug': category.slug,
                    'name': category.name,
                    'image': category.image,
                    'has_conflict': has_conflict,
                    'is_selected': component is not None
                })

            if component:
                selected_slugs.append(category.slug)

        # Проверка обязательных компонентов
        missing = [
            cat['name'] for cat in required_categories
            if not cat['is_selected']
               and cat['slug'] in ['processor', 'motherboard', 'psu', 'case']
        ]

        if missing:
            messages.error(request, f"Обязательные компоненты: {', '.join(missing)}")

        return render(request, "configurator/builder/step_category.html", {
            'required_categories': required_categories,
            'cpu_cooling_categories': cpu_cooling_categories,
            'storage_categories': storage_categories,
            'optional_categories': optional_categories,
            'selected_components': [
                {
                    'product': bc.product,
                    'quantity': bc.quantity,
                    'has_conflict': any(
                        k in compatibility_errors
                        for k in [bc.product.category.slug[:-1], 'system']
                    )
                } for bc in selected_components
            ],
            'total_conflicts': total_conflicts,
            'selected_categories_slugs': selected_slugs,
            'missing_components': missing,
            'progress': build.calculate_progress(),  # Используем метод модели
            'step': 1,
            'compatibility_errors': checker.validate(),
        })


# apps/configurator/views/builder.py
class ComponentSelectionView(LoginRequiredMixin, View):
    """Выбор компонентов с учётом совместимости"""

    def _get_compatibility_filters(self, category, selected_components):
        filters = {}

        # Для ОЗУ: фильтр по типу и частоте памяти
        if category.slug == "rams":
            mb = next((c for c in selected_components if c.category.slug == "motherboards"), None)
            if mb:
                mb_specs = mb.motherboardspecs_specs
                filters.update({
                    "memory_type": mb_specs.memory_type,
                    "frequency__lte": mb_specs.oc_memory_freq or mb_specs.base_memory_freq
                })

        # Для SSD M.2: проверка ключа и версии PCIe
        if category.slug == "m2ssds":
            mb = next((c for c in selected_components if c.category.slug == "motherboards"), None)
            if mb:
                filters.update({
                    "m2_key": "M",
                    "interface__startswith": f"PCIe {mb.motherboardspecs_specs.pcie_version}"
                })

        # Для кулеров: совместимость сокетов
        if category.slug == "coolers":
            cpu = next((c for c in selected_components if c.category.slug == "processors"), None)
            if cpu:
                cpu_socket = cpu.processorspecs_specs.socket
                filters["socket_support__icontains"] = cpu_socket

        # Для видеокарт: проверка длины и разъёмов питания
        if category.slug == "videocards":
            case = next((c for c in selected_components if c.category.slug == "cases"), None)
            if case:
                filters["length__lte"] = case.casespecs_specs.max_gpu_length

        return filters

    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        build_id = request.session.get("current_build_id")
        build = PCBuild.objects.get(id=build_id) if build_id else None

        selected_components = build.components.all() if build else []
        compatibility_filters = self._get_compatibility_filters(category, selected_components)

        products = Product.objects.filter(
            category=category,
            is_active=True,
            **compatibility_filters
        ).prefetch_related('images')

        return render(request, "configurator/builder/step_component.html", {
            "category": category,
            "products": products,
            "compatibility_filters": compatibility_filters
        })


# apps/configurator/views/builder.py
class BuildSummaryView(LoginRequiredMixin, View):
    def get(self, request):
        build_id = request.session.get("current_build_id")
        build = get_object_or_404(PCBuild, id=build_id)
        errors = CompatibilityChecker(build.components.all()).validate()
        return render(request, "configurator/builder/summary.html", {
            "build": build,
            "errors": errors,
            "progress": 100,
            "step": 3
        })

    def post(self, request):
        build_id = request.session.get("current_build_id")
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)
        errors = CompatibilityChecker(build.components.all()).validate()

        if build.buildcomponent_set.count() == 0:
            messages.error(request, "Добавьте компоненты перед сохранением.")
            return redirect("configurator:select_category")

        # Добавление в корзину
        if "add_to_cart" in request.POST and not errors:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            for component in build.buildcomponent_set.all():  # Исправлено: buildcomponent_set вместо components
                CartItem.objects.get_or_create(
                    cart=cart,
                    product=component.product,
                    defaults={"quantity": component.quantity}
                )
            return redirect("cart:detail")

        # Сохранение сборки
        if "save_build" in request.POST and not errors:
            build.is_public = False
            build.is_verified = False  # Добавлено явное сохранение статуса
            build.title = request.POST.get("build_title", build.title)
            build.save()
            messages.success(request, "Сборка сохранена в личном кабинете.")
            request.session.pop("current_build_id", None)  # Очистка сессии
            return redirect("configurator:my_builds")

        # Публикация
        if "publish_build" in request.POST and not errors:
            build.is_public = True
            build.title = request.POST.get("build_title", build.title)
            build.save()
            messages.success(request, "Сборка опубликована в каталоге.")
            request.session.pop("current_build_id", None)  # Очистка сессии
            return redirect("configurator:public_builds")

        # Если есть ошибки, остаемся на странице
        return render(request, "configurator/builder/summary.html", {
            "build": build,
            "errors": errors
        })


# apps/configurator/views/builder.py
class BuildEditView(LoginRequiredMixin, View):
    """Редактирование существующей сборки."""

    def dispatch(self, request, *args, **kwargs):
        build = get_object_or_404(PCBuild, id=kwargs["build_id"])
        if build.user != request.user and not build.is_public:
            raise PermissionDenied("Вы не можете редактировать эту сборку.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)
        request.session["current_build_id"] = build_id  # Сохраняем ID в сессии
        return redirect("configurator:select_category")

    def post(self, request, build_id):
        build = get_object_or_404(PCBuild, id=build_id, user=request.user)
        # Удаляем старые компоненты через промежуточную модель
        BuildComponent.objects.filter(build=build).delete()

        # Добавляем новые компоненты из сессии
        new_build_id = request.session.get("current_build_id")
        if new_build_id:
            new_components = BuildComponent.objects.filter(build_id=new_build_id)
            for component in new_components:
                BuildComponent.objects.create(
                    build=build,
                    product=component.product,
                    quantity=component.quantity
                )

        build.title = request.POST.get("build_title", "")
        build.save()
        return redirect("configurator:summary")


# Для получения обновлённых ошибок совместимости
class CompatibilityStatusView(LoginRequiredMixin, View):
    def get(self, request):
        build_id = request.session.get("current_build_id")
        build = get_object_or_404(PCBuild, id=build_id)
        return JsonResponse({
            "errors": build.compatibility_errors,
            "total_conflicts": len(build.compatibility_errors),
            "progress": build.calculate_progress()
        })


# Для получения актуальной цены
class PriceUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        build_id = request.session.get("current_build_id")
        build = get_object_or_404(PCBuild, id=build_id)
        return JsonResponse({"total_price": build.total_price})
