from libs.aws.sgs import get_security_groups
from libs.db_context import DBContext
from models.sgs import FreeSgs
from settings import settings


def sgs_sync_cmdb():
    """没有和任何资源关联的安全组数据同步"""
    sgs_list = get_security_groups()
    with DBContext('w') as session:
        session.query(FreeSgs).delete(synchronize_session=False)  # 清空数据库的所有记录
        for sgs in sgs_list:
            security_group_id = sgs.get("GroupId", "")
            security_group_name = sgs.get("GroupName", "")
            vpc_id = sgs.get("VpcId", "")
            owner_id = sgs.get("OwnerId", "")
            description = sgs.get("Description", "")
            to_port = sgs.get("ToPort", "")
            ip_permissions_egress = str(sgs.get("IpPermissionsEgress", ""))
            ip_permissions = str(sgs.get("IpPermissions", ""))
            is_used = sgs.get("is_used", 1)
            new_sgs = FreeSgs(
                security_group_id=security_group_id, security_group_name=security_group_name, vpc_id=vpc_id,
                owner_id=owner_id, description=description, to_port=to_port, is_used=is_used,
                ip_permissions_egress=ip_permissions_egress, ip_permissions=ip_permissions
            )
            session.add(new_sgs)
        session.commit()


if __name__ == '__main__':
    pass