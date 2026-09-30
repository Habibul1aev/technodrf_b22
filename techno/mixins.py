from rest_framework import viewsets

class SerializerClassesMixins:
    serializer_classes = {}

    def get_serializer_class(self):
        serializer_class = self.serializer_classes.get(self.action, self.serializer_class)

        if self.action in ['partial_update', 'update_partial']:
            serializer_class = self.serializer_classes.get('update', self.serializer_class)

        assert serializer_class is not None, f'There is no serializer for "{self.action}" action.'

        return serializer_class


class PermissionByActionMixin:
    permission_classes_by_action = {}

    def get_permissions(self):
        permission_classes = self.permission_classes_by_action.get(self.action, self.permission_classes)

        if self.action in ['partial_update', 'update_partial']:
            permission_classes = self.permission_classes_by_action.get('update', self.permission_classes)

        assert permission_classes is not None, f'There is no permissions for "{self.action}" action.'
        assert type(permission_classes) is list, f'Permissions for "{self.action}" action should ' \
                                                 f'contain list of Permissions.'

        return [permission() for permission in permission_classes]


class ProModelViewSet(SerializerClassesMixins, PermissionByActionMixin, viewsets.ModelViewSet):
    pass







