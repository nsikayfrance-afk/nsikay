from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordRecoveryRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        max_length=320,
        trim_whitespace=True,
    )


class PasswordRecoveryVerifySerializer(serializers.Serializer):
    recovery_id = serializers.IntegerField(
        min_value=1,
    )

    code = serializers.CharField(
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )


class PasswordRecoveryResetSerializer(serializers.Serializer):
    recovery_id = serializers.IntegerField(
        min_value=1,
    )

    code = serializers.CharField(
        min_length=6,
        max_length=6,
        trim_whitespace=True,
    )

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        min_length=8,
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        min_length=8,
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password_confirm":
                    "Les mots de passe ne correspondent pas."
                }
            )

        validate_password(
            attrs["password"]
        )

        return attrs
