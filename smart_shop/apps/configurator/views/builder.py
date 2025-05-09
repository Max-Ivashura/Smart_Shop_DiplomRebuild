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
            build = PCBuild.objects.create(user=request.user)
            request.session["current_build_id"] = build.id
        else:
            build = get_object_or_404(PCBuild, id=build_id)

        # Удаляем компоненты той же категории через промежуточную модель
        BuildComponent.objects.filter(
            build=build,
            product__category=product.category
        ).delete()

        # Добавляем новый компонент с явным созданием через BuildComponent
        BuildComponent.objects.create(
            build=build,
            product=product,
            quantity=1  # Указываем значение по умолчанию
        )

        return redirect("configurator:select_category")


# apps/configurator/views/builder.py
class ConfiguratorStartView(LoginRequiredMixin, View):
    """Создает новую сборку и перенаправляет на выбор категории."""

    def get(self, request):
        # Создаем новую сборку
        build = PCBuild.objects.create(user=request.user)
        # Сохраняем ID сборки в сессии
        request.session["current_build_id"] = build.id
        # Перенаправляем на выбор категории
        return redirect("configurator:select_category")

# apps/configurator/views/builder.py
class ComponentCategoryView(LoginRequiredMixin, View):
    """Выбор категории компонента с визуализацией конфликтов"""

    REQUIRED_SLUGS = [
        'processor',
        'motherboard',
        'ram',
        'psu',
        'case'
    ]

    def get(self, request):
        # Получаем текущую сборку
        build_id = request.session.get('current_build_id')
        if not build_id:
            return redirect('configurator:start')

        build = PCBuild.objects.get(id=build_id)
        selected_components = build.buildcomponent_set.select_related('product').all()

        # Проверяем совместимость всей сборки
        checker = CompatibilityChecker([bc.product for bc in selected_components])
        compatibility_errors = checker.validate()

        # Формируем данные для категорий
        categories_data = []
        selected_slugs = []
        total_conflicts = 0

        for category in Category.objects.filter(slug__in=self.REQUIRED_SLUGS):
            component = selected_components.filter(product__category=category).first()
            has_conflict = any(
                error_key in compatibility_errors
                and error_key == category.slug[:-1]  # processors -> processor
                for error_key in compatibility_errors
            )

            if has_conflict:
                total_conflicts += 1

            categories_data.append({
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
            cat['name'] for cat in categories_data
            if not cat['is_selected']
               and cat['slug'] in ['processors', 'motherboards', 'psus', 'cases']
        ]

        if missing:
            messages.error(request, f"Обязательные компоненты: {', '.join(missing)}")

        return render(request, "configurator/builder/step_category.html", {
            # Основные данные
            'categories': categories_data,
            'selected_components': [
                {
                    'product': bc.product,
                    'has_conflict': any(
                        k in compatibility_errors
                        for k in [bc.product.category.slug[:-1], 'system']
                    )
                } for bc in selected_components
            ],

            # Статусы
            'total_conflicts': total_conflicts,
            'selected_categories_slugs': selected_slugs,
            'missing_components': missing,

            # Прогресс
            'progress': self._calculate_progress(selected_slugs),
            'step': 1
        })

    def _calculate_progress(self, selected_slugs):
        """Рассчитывает прогресс сборки в %"""
        required_count = len(self.REQUIRED_SLUGS)
        selected = len([s for s in selected_slugs if s in self.REQUIRED_SLUGS])
        return int((selected / required_count) * 100)


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
        build = get_object_or_404(PCBuild, id=request.session.get("current_build_id"))
        errors = CompatibilityChecker(build.components.all()).validate()

        if any(key in errors for key in ["cpu", "motherboard", "ram", "psu", "case"]):
            return render(request, "configurator/builder/summary.html", {
                "build": build,
                "errors": errors,
                "progress": 100,
                "step": 3
            })

        # Добавление в корзину
        if "add_to_cart" in request.POST:
            if errors:
                return render(request, "configurator/builder/summary.html", {
                    "build": build,
                    "errors": errors,
                    "progress": 100,
                    "step": 3
                })

            cart, _ = Cart.objects.get_or_create(user=request.user)
            for component in build.components.all():
                CartItem.objects.get_or_create(
                    cart=cart,
                    product=component,
                    defaults={"quantity": 1}
                )
            return redirect("cart:detail")

        # Сохранение сборки
        build.is_public = "is_public" in request.POST
        build.save()
        return redirect("configurator:public_builds")


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
        # Удаляем старые компоненты
        build.components.clear()
        # Добавляем новые (логика из сессии)
        new_components = PCBuild.objects.get(id=request.session.get("current_build_id")).components.all()
        build.components.set(new_components)
        build.save()
        return redirect("configurator:summary")
