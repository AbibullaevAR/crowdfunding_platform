from itertools import chain
from collections import defaultdict

from rest_framework.response import Response


class ProjectListWithImageMixin:

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        all_images = list(chain(*[project.images.all() for project in queryset]))

        context = self.get_serializer_context()
        context['images'] = defaultdict(list)
        
        [
            context['images'][image.project.id].append(link)
            for image, link in self.images_link_func(all_images)
        ]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context=context)
        return Response(serializer.data)