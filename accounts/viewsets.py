from rest_framework import mixins, viewsets


class CreateOnlyViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    A viewset that provides only `create()` actions.
    """
    pass
