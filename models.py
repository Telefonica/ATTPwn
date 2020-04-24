from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship



class Warriors(db.Model):
	#tabla warriors que se conectaron en algun momento
	__tablename__ = 'warrior'
	idwarrior = Column(String(8), primary_key=True)
	os = Column(String(30),nullable=False)
	arch = Column(String(10),nullable=False)
	name = Column(String(20),nullable=False)
	pid = Column(String(8),nullable=False)
	lastseen = Column(DateTime,nullable=False)

	#def idwarrior(self):
		#return self.idwarrior

	def __repr__(self):
		return (u'<{self.__class__.__name__}: {self.idwarrior}>'.format(self=self))
