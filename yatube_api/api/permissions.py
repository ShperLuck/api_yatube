from rest_framework import permissions

# Создаём класс разрешений
class IsAuthorOrReadOnly(permissions.BasePermission):
    # Здесь проверяем на доступ к конкретному объекту
    def has_object_permission(self, request, view, obj):
        
        # Типа доступ, разрешения
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
