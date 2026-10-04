from django.contrib import admin

from .models import (
    MembershipType,
    Member,
    Subscription,
    Donation,
    MembershipApplication,
    MemberCard,
    MembershipAuditLog,
)


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "contribution_required",
    )
    search_fields = ("name",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "membership_type",
        "status",
        "joined_at",
    )
    list_filter = (
        "status",
        "membership_type",
    )
    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "member",
        "amount",
        "currency",
        "payment_status",
        "paid_at",
    )
    list_filter = (
        "payment_status",
        "currency",
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "amount",
        "currency",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "membership_type",
        "status",
        "created_at",
        "reviewed_at",
    )
    list_filter = (
        "status",
        "membership_type",
    )
    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(MemberCard)
class MemberCardAdmin(admin.ModelAdmin):
    list_display = (
        "member_number",
        "member",
        "status",
        "issued_at",
        "expires_at",
    )
    list_filter = ("status",)
    search_fields = (
        "member_number",
        "member__user__username",
    )
    readonly_fields = (
        "member_number",
        "qr_token",
        "issued_at",
        "created_at",
        "updated_at",
    )


@admin.register(MembershipAuditLog)
class MembershipAuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "action",
        "user",
        "member",
        "reference",
        "created_at",
    )
    list_filter = ("action",)
    search_fields = (
        "reference",
        "user__username",
    )
    readonly_fields = (
        "created_at",
    )
