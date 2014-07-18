import sqlalchemy as sa
from datetime import datetime
import uuid
import hashlib
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_unique_hash():
    return hashlib.md5(str(uuid.uuid4())).hexdigest()


class Snapshot(Base):
    __tablename__ = 'snapshot'
    id = sa.Column(sa.Integer, sa.Sequence('snapshot_id_seq'), primary_key=True)
    snapshot_name = sa.Column(sa.String(255), nullable=False)
    project_name = sa.Column(sa.String(255), nullable=False)
    hash = sa.Column(sa.String(32), nullable=False, default=get_unique_hash)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "Snapshot(name=%r, name=%r)" % (
            self.table_name,
            self.name
        )


class Table(Base):
    __tablename__ = 'table'
    id = sa.Column(sa.Integer, sa.Sequence('table_id_seq'), primary_key=True)
    table_name = sa.Column(sa.String(255), nullable=False)
    snapshot_id = sa.Column(sa.Integer, sa.ForeignKey(Snapshot.id), nullable=False)
    snapshot = sa.orm.relationship(Snapshot, backref='tables')
    slave_pid = sa.Column(sa.Integer, nullable=True)

    def get_table_name(self, postfix):
        return 'stellar_%s_%s_%s' % (
            self.name,
            self.snapshot.hash,
            postfix
        )

    def __repr__(self):
        return "Snapshot(table_name=%r, name=%r)" % (
            self.table_name,
            self.name
        )
