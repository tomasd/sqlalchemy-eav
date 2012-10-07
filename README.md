Sqlalchemy EAV
==============

Provides base classes for Entity-Attribute-Value model
(http://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model)
# Attribute,
# AttributeValue
# AttributeCodebook

Attribute
-----
Attribute is a template for values. It defines the key (ID), name of the
attribute, it's type and multiplicity.

Attribute can be of these types:
# int
# char
# boolean
# decimal
# datetime
# date
# codebook - value from predefined list (see AttributeCodebook)

You have to define __value__ property in your subclass with reference to your
custom AttributeValue class.

AttributeValue
-----
AttributeValue is holder of the actual value. Each type has separate column,
so you can use your database at max.

To find actual column used for storing value use Attribute.value_column. It's
useful for queries.

For simple assignment and getting the value use value property.


AttributeCodebook
-----
AttributeCodebook defines predefined list of values which can be hold by
Attribute of type codebook

Usage
=====

        class AttributeValue(eav.AttributeValue, self.Model):
            __tablename__ = 'attribute_value'
            customer_id = sa.Column(None, sa.ForeignKey('customer.id'))
            customer = orm.relationship('Customer',
                                        backref=orm.backref('attributes'))

        class Attribute(eav.Attribute, self.Model):
            __tablename__ = 'attribute'
            __value__ = AttributeValue

        class AttributeCodebook(eav.AttributeCodebook, self.Model):
            __tablename__ = 'attribute_codebook'
