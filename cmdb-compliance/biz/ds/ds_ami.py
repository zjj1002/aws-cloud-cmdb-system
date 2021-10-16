from libs.aws.ami import get_ami_list
from libs.db_context import DBContext
from models.ami import Ami


def ami_sync_cmdb():
    """ami数据同步"""
    ami_list = get_ami_list()
    with DBContext('w') as session:
        session.query(Ami).delete(synchronize_session=False)  # 清空数据库的所有记录
        for ami in ami_list:
            ami_id = ami.get("ImageId", "")
            # ami_name = ami.get("Name", "")
            # image_location = ami.get("ImageLocation", "")
            # owner_id = ami.get("OwnerId", "")
            # image_type = ami.get("ImageType", "")
            # creation_date = str(ami.get("CreationDate", ""))
            # state = ami.get("State", "")
            # architecture = ami.get("Architecture", "")
            new_ami = Ami(
                ami_id=ami_id
            )
            session.add(new_ami)
        session.commit()


if __name__ == '__main__':
    pass