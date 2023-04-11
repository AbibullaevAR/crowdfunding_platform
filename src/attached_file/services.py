from django.db.models import QuerySet

from attached_file.models import Image
from attached_file.helpers import ExternalStorageManage


def create_image_for_project(project, available_formats: list[str]) -> list[str]:

    images: list[Image] = [Image.objects.create(project=project, available_format=available_format) for available_format in available_formats]
    storage = ExternalStorageManage()
    return [storage.get_upload_link(str(image.id) + image.available_format) for image in images]


def get_download_link_for_images(images: QuerySet[Image]) -> list[QuerySet[Image], list[str]]:

    storage = ExternalStorageManage()
    download_links = storage.get_download_links([str(image.id) + image.available_format for image in images])

    return zip(images, download_links)