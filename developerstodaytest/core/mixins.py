class ViewsetSerializerMixin:
    """
    Add functionallity to map serializer class to viewset's actions

    SimpleRouter default actions:
        list, create, retrieve, update, partial_update, destroy
    """

    serializer_class = None

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' a `serializer_class` attribute must be "
            "`rest_framework.serializers.Serailizer` class or be a dict, like "
            "SerializerClass: ['list', 'of', 'actions']" % self.__class__.__name__
        )

        if isinstance(self.serializer_class, dict):
            for serializer_class, actions in self.serializer_class.items():
                if self.action in actions:
                    return serializer_class

            raise Exception(
                "'%s' has no serializer class found for '%s' action"
                % (self.__class__.__name__, self.action)
            )
        else:
            return self.serializer_class
