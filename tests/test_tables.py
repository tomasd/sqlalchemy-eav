from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import eav


class ModelTest(TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://')
        self.Model = declarative_base(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_model(self):
        class AttributeValue(eav.AttributeValue, self.Model):
            __tablename__ = 'attribute_value'

        class Attribute(eav.Attribute, self.Model):
            __tablename__ = 'attribute'
            __value__ = AttributeValue

        class AttributeCodebook(eav.AttributeCodebook, self.Model):
            __tablename__ = 'attribute_codebook'

        self.Model.metadata.create_all()

        attr = Attribute(id='custom', name='Custom')
        value = AttributeValue(attribute=attr, value='xxx')

        self.session.add(attr)
        self.session.add(value)
        self.session.commit()

        self.assertEquals(1, self.session.query(AttributeValue).count())
        self.assertEquals('xxx',
                          self.session.query(AttributeValue).first().value)

        self.assertIs(AttributeValue.__table__.c.char_value, attr.value_column)
