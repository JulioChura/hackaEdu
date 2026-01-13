from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializador básico del usuario"""
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'nombre', 'apellido', 'telefono', 'avatar', 'fecha_nacimiento')
        read_only_fields = ('id',)


class UserDetailSerializer(UserSerializer):
    """Serializador detallado del usuario"""
    google_profile = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('date_joined', 'is_active', 'email_verificado', 'google_profile')
        read_only_fields = UserSerializer.Meta.read_only_fields + ('date_joined', 'is_active', 'email_verificado')
    
    def get_google_profile(self, obj):
        """Incluir datos de Google si el usuario tiene cuenta vinculada"""
        if obj.has_google_account():
            return {
                'google_id': obj.google_id,
                'picture': obj.google_picture,
                'has_google': True
            }
        return {'has_google': False}


class RegisterSerializer(serializers.ModelSerializer):
    """Serializador para registro de usuarios"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'apellido', 'password', 'password_confirm', 'telefono')

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden'})
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            telefono=validated_data.get('telefono', ''),
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializador para cambiar contraseña"""
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data.pop('new_password_confirm'):
            raise serializers.ValidationError({'new_password': 'Las contraseñas no coinciden'})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Contraseña actual incorrecta')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
