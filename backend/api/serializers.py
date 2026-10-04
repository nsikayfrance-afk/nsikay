from django.contrib.auth import get_user_model

from rest_framework import serializers

from nsikay_profiles.models import NsikayProfile


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "date_joined",
        ]


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    password_confirm = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    personal_photo = serializers.ImageField(
        write_only=True,
        required=True,
    )

    identity_document_photo = serializers.ImageField(
        write_only=True,
        required=True,
    )

    identity_with_document_photo = serializers.ImageField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
            "personal_photo",
            "identity_document_photo",
            "identity_with_document_photo",
        ]

    def validate_username(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Le nom d'utilisateur est obligatoire."
            )

        if User.objects.filter(
            username__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Ce nom d'utilisateur existe déjà."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        if value and User.objects.filter(
            email__iexact=value
        ).exists():
            raise serializers.ValidationError(
                "Cette adresse e-mail existe déjà."
            )

        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": (
                    "Les mots de passe ne correspondent pas."
                )
            })

        return attrs

    def create(self, validated_data):

        personal_photo = validated_data.pop(
            "personal_photo"
        )

        identity_document_photo = validated_data.pop(
            "identity_document_photo"
        )

        identity_with_document_photo = validated_data.pop(
            "identity_with_document_photo"
        )

        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        NsikayProfile.objects.create(
            user=user,
            profile_type="person",
            display_name=(
                f"{user.first_name} {user.last_name}"
            ).strip() or user.username,
            is_primary=True,
            personal_photo=personal_photo,
            identity_document_photo=identity_document_photo,
            identity_with_document_photo=(
                identity_with_document_photo
            ),
            certification_required=True,
            certification_status="pending",
        )

        return user
