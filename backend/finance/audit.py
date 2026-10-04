from finance.models import AuditLog



def create_audit(

    user,

    action,

    description,

    ip=None

):


    return AuditLog.objects.create(

        user=user,

        action=action,

        description=description,

        ip_address=ip

    )


