from rest_framework import serializers
from auth_.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'avatar')

    def validate_email(self, email):
        if '/^[A-Z0-9._%+-]+@[A-Z0-9-]+.+.[A-Z]{2,4}$/i' in email:
            raise serializers.ValidationError("The email is not entered correctly")
        return email

    def validate_password(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError('Passwords must match')
        return value


class CustomUserSerializerAll(CustomUserSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserSerializerForComment(CustomUserSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name')
