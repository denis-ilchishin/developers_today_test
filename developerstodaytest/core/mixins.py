from rest_framework import status
from rest_framework.response import Response


class ViewsetSerializerMixin:
    """
    Add functionallity to map serializer class to viewset's actions

    SimpleRouter default actions:
        list, create, retrieve, update, partial_update, destroy
    """

    serializer_class = None

    def get_serializer_class(self, action=None):
        assert self.serializer_class is not None, (
            "'%s' a `serializer_class` attribute must be "
            "`rest_framework.serializers.Serailizer` class or be a dict, like "
            "SerializerClass: ['list', 'of', 'actions']" % self.__class__.__name__
        )

        action = action or self.action

        if isinstance(self.serializer_class, dict):
            for serializer_class, actions in self.serializer_class.items():
                if action in actions:
                    return serializer_class

            raise Exception(
                "'%s' has no serializer class found for '%s' action"
                % (self.__class__.__name__, action)
            )
        else:
            return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        action = kwargs.pop("action", None)
        serializer_class = self.get_serializer_class(action)
        kwargs.setdefault("context", self.get_serializer_context())

        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = self.get_serializer(instance, action="retrieve")
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if not partial:
            serializer = self.get_serializer(instance, action="retrieve")

        return Response(serializer.data)
