from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
import sqlalchemy.orm as orm
from app import db


def foreign_key_column(name, type_, target, nullable=False):
    """Construct a foreign key column for a table.

    ``name`` is the column name. Pass ``None`` to omit this arg in the
    ``Column`` call; i.e., in Declarative classes.

    ``type_`` is the column type.

    ``target`` is the other column this column references.

    ``nullable``: pass True to allow null values. The default is False
    (the opposite of SQLAlchemy's default, but useful for foreign keys).
    """
    fk = db.ForeignKey(target)
    if name:
        return db.Column(name, type_, fk, nullable=nullable)
    else:
        return db.Column(type_, fk, nullable=nullable)

        



class Warrior_DB(db.Model):
    __tablename__ = "Warrior"
    IDWarrior                   = db.Column(db.Integer, primary_key= True, nullable=False)
    State                       = db.Column(db.String(100))
    Legacy                      = db.Column(db.String(100))
    Alias                       = db.Column(db.String(100),nullable=False)
    Os                          = db.Column(db.String(100))
    Arch                        = db.Column(db.String(100))
    Name                        = db.Column(db.String(100))
    PID                         = db.Column(db.String(100))
    Lastseen                    = db.Column(db.String(100))
    IP                          = db.Column(db.String(100))

class Technique_DB(db.Model):
    __tablename__ = "Technique"
    IDTech                   = db.Column(db.Integer, primary_key= True, nullable=False)
    URL_Mitre                = db.Column(db.String(500))
    Name                     = db.Column(db.String(100))
    IDMitre                  = db.Column(db.String(100), unique=True, nullable=False)     
    # intels                   = orm.relationship("Inteligence", order_by="Inteligence.IDIntel")

class Tactic_DB(db.Model):
    __tablename__ = "Tactic"
    IDTactic                 = db.Column(db.Integer, primary_key= True, nullable=False)
    URL_Mitre                = db.Column(db.String(100))
    Name                     = db.Column(db.String(100))
    Description              = db.Column(db.String(500))
    IDMitre                  = db.Column(db.String(100), unique=True, nullable=False) 
    # intels                   = orm.relationship("Inteligence", order_by="Inteligence.IDIntel") 

class Inteligence_DB(db.Model):
    __tablename__ = "Inteligence"
    IDIntel                  = db.Column(db.Integer, primary_key= True, nullable=False)
    IDTech                   = foreign_key_column("IDTech", db.String, "Technique.IDMitre")
    IDTactic                 = foreign_key_column("IDTactic", db.String, "Tactic.IDMitre")
    Function                 = db.Column(db.String(500))    
    Terminated               = db.Column(db.String(100))

class Threat_DB(db.Model):
    __tablename__ = "Threat"
    IDthreat                 = db.Column(db.Integer, primary_key= True, nullable=False)
    Created                  = db.Column(db.String(100))
    Modified                 = db.Column(db.String(100))
    Name                     = db.Column(db.String(100))
    Description              = db.Column(db.String(1000))
    Windows                  = db.Column(db.String(100))
    MacOS                    = db.Column(db.String(100))
    Linux                    = db.Column(db.String(100))


class Plan_DB(db.Model):
    __tablename__ = "Plan"
    IDPlan                   = db.Column(db.Integer, primary_key= True, nullable=False)
    IDThreat                 = foreign_key_column("IDThreat", db.Integer, "Threat.IDthreat")
    Name                     = db.Column(db.String(100))
    Description              = db.Column(db.String(500))

class Task_DB(db.Model):
    __tablename__ = "Task"
    IDTask                   = db.Column(db.Integer, primary_key= True, nullable=False)
    IDPlan                   = foreign_key_column("IDPlan", db.Integer, "Plan.IDPlan")
    IDIntel                  = foreign_key_column("IDIntel", db.Integer, "Inteligence.IDIntel")
    Orden                    = db.Column(db.String(100))

class Directive_DB(db.Model):
    __tablename__ = "Directive"
    IDDirective                     = db.Column(db.Integer, primary_key = True, nullable=False)
    IDWarrior                       = foreign_key_column("IDWarrior", db.Integer, "Warrior.IDWarrior")
    IDTask                          = foreign_key_column("IDTask", db.Integer, "Task.IDTask")
    Result                          = db.Column(db.String(2000))
    Done                            = db.Column(db.String(100))
    Good                            = db.Column(db.String(100))
    Privilege                       = db.Column(db.String(100))

class DataStore_DB(db.Model):
    __tablename__ = "DataStore"
    IDData                          = db.Column(db.Integer, primary_key= True, nullable=False)
    IDWarrior                          = foreign_key_column("IDWarrior", db.Integer, "Warrior.IDWarrior")
    User                            = db.Column(db.String(100))
    IP                              = db.Column(db.String(100))
    Password                        = db.Column(db.String(100))
    NTLM                            = db.Column(db.String(100))
    LM                              = db.Column(db.String(100))
    Port                            = db.Column(db.String(100))


class Version_DB(db.Model):
    __tablename__       = "migrate_version"
    repository_id       = db.Column(db.String(250), primary_key= True)
    repository_path     = db.Column(db.Text )
    version             = db.Column(db.Integer)
    
