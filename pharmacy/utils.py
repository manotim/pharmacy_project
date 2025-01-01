from .models import AuditLog

def create_audit_log(drug, action, quantity_changed, performed_by):
    AuditLog.objects.create(
        drug=drug,
        action=action,
        quantity_changed=quantity_changed,
        performed_by=performed_by,
    )
