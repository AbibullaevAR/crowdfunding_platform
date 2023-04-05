from attached_file.models import Image
from attached_file.helpers import ExternalStorageManage


def create_image_for_project(project, available_formats: list[str]) -> list[str]:

    images: list[Image] = [Image.objects.create(project=project, available_format=available_format) for available_format in available_formats]
    storage = ExternalStorageManage()
    return [storage.get_upload_link(str(image.id) + image.available_format) for image in images]