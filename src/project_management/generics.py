from functools import partial

from project_management.mixins import ProjectListWithImageMixin

from rest_framework.generics import GenericAPIView


class ProjectListWithImageAPIView(ProjectListWithImageMixin, GenericAPIView):

    images_link_func = None

    def __new__(cls, *args, **kwargs):
        cls.images_link_func = partial(cls.images_link_func)
        instance = super().__new__(cls)
        return instance

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)