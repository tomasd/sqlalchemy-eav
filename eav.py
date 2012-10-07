from collections import namedtuple
import sqlalchemy as sa
from sqlalchemy.ext.declarative import AbstractConcreteBase, declared_attr
import sqlalchemy.orm as orm


AttributeType = namedtuple('AttributeType', 'id label sa_type')
ATTRIBUTE_TYPES = (AttributeType('int', 'Integer', sa.Integer),
                   AttributeType('char', 'Character', sa.String),
                   AttributeType('boolean', 'Boolean', sa.Boolean),
                   AttributeType('decimal', 'Decimal', sa.Numeric),
                   AttributeType('datetime', 'DateTime', sa.DateTime),
                   AttributeType('date', 'Date', sa.Date),
                   AttributeType('codebook', 'Codebook', sa.Integer))


def get_attribute_type_dict():
    return {a.id: a for a in ATTRIBUTE_TYPES}


def get_attribute_type_ids():
    return [a.id for a in ATTRIBUTE_TYPES]


class Attribute(object):
    id = sa.Column(sa.String(255), primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    type = sa.Column(
        sa.Enum(*get_attribute_type_ids(), name='attribute_types'),
        default='char',
        server_default='char')
    multiple = sa.Column(sa.Boolean, server_default='false', default=False)

    def __init__(self, id, name, type='char', multiple=False):
        super(Attribute, self).__init__(id=id, name=name, type=type,
                                        multiple=multiple)

    @property
    def value_column(self):
        return self.__value__.__table__.c['%s_value' % self.type]

    @property
    def sqlalchemy_type(self):
        return get_attribute_type_dict()[self.type].sa_type


class AttributeValue(object):
    id = sa.Column(sa.Integer, primary_key=True)

    def __init__(self, **kwargs):
        value = kwargs.pop('value', None)
        super(AttributeValue, self).__init__(**kwargs)

        if value is not None:
            self.value = value

    @declared_attr
    def attribute_id(self):
        return sa.Column(None,
                         sa.ForeignKey('attribute.id', ondelete='CASCADE'),
                         nullable=False)

    @declared_attr
    def attribute(self):
        return orm.relationship('Attribute',
                                lazy='joined',
                                backref=orm.backref('attributes',
                                                    cascade='all'))

    char_value = sa.Column(sa.String)
    int_value = sa.Column(sa.Integer)
    boolean_value = sa.Column(sa.Boolean)
    decimal_value = sa.Column(sa.Numeric(10, 2))
    datetime_value = sa.Column(sa.DateTime)
    date_value = sa.Column(sa.Date)
    codebook_value = sa.Column(sa.String(255))

    @declared_attr
    def codebook(self):
        return orm.relationship('AttributeCodebook',
                                backref=orm.backref('attributes', ))

    @declared_attr
    def __table_args__(self):
        return (
            sa.ForeignKeyConstraint(
                ['attribute_id', 'codebook_value'],
                ['attribute_codebook.attribute_id',
                 'attribute_codebook.id']),
            )

    @property
    def value(self):
        return getattr(self, '%s_value' % self.attribute.type)

    @value.setter
    def value(self, value):
        assert self.attribute.type, 'Type must be filled'
        setattr(self, '%s_value' % self.attribute.type, value)


class AttributeCodebook(object):
    @declared_attr
    def attribute_id(self):
        return sa.Column(None,
                         sa.ForeignKey('attribute.id', ondelete='CASCADE'),
                         nullable=False)

    @declared_attr
    def attribute(self):
        return sa.orm.relationship('Attribute',
                                   backref=orm.backref('codebooks'))

    id = sa.Column(sa.String(255))
    name = sa.Column(sa.String(255), nullable=False)

    @declared_attr
    def __table_args__(self):
        return (sa.PrimaryKeyConstraint('attribute_id', 'id'),)




