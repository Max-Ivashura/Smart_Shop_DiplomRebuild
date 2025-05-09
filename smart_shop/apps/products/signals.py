from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import logging
from .models import Product
from .models.specs import (
    CaseSpecs, CaseFanSpecs, CoolerSpecs, HardDriveSpecs,
    M2SSDSpecs, MotherboardSpecs, ProcessorSpecs, PSUSpecs,
    RAMSpecs, SSDSpecs, ThermalPasteSpecs, VideoCardSpecs,
    WaterCoolingSpecs
)

logger = logging.getLogger(__name__)

SPECS_MAPPING = {
    'case': CaseSpecs,
    'casefan': CaseFanSpecs,
    'cooler': CoolerSpecs,
    'hdd': HardDriveSpecs,
    'm2ssd': M2SSDSpecs,
    'motherboard': MotherboardSpecs,
    'processor': ProcessorSpecs,
    'psu': PSUSpecs,
    'ram': RAMSpecs,
    'ssd': SSDSpecs,
    'thermalpaste': ThermalPasteSpecs,
    'videocard': VideoCardSpecs,
    'watercooling': WaterCoolingSpecs,
}


@receiver(post_save, sender=Product)
def create_product_specs(sender, instance, created, **kwargs):
    if not created:
        return

    category_slug = instance.category.slug
    specs_class = SPECS_MAPPING.get(category_slug)

    if specs_class:
        # Удаляем старые спецификации, если они есть
        if hasattr(instance, f"{category_slug}specs_specs"):
            getattr(instance, f"{category_slug}specs_specs").delete()
        # Создаем новые
        specs_class.objects.create(product=instance)
    else:
        logger.warning(f"No specs class for category: {category_slug}")