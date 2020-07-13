#!flask/bin/python 
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from config import SQLALCHEMY_DATABASE_DIR
from config import SQLALCHEMY_DATABASE_VERSION


from app import db
import data as ins_records
import os.path
import time
# import db_upgrade as upgrade_db
def create_database():
    iniciar = False
    if not os.path.exists(SQLALCHEMY_DATABASE_DIR):
        iniciar = True
        db.create_all()
    # time.sleep(3)
    # ins_records.insert_tech()
    response = False
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        ins_records.insert_version()        
        time.sleep(0.5)
    if iniciar:
        ins_records.insert_tech()
        ins_records.insert_tactic()
        ins_records.insert_inteligence()
        ins_records.insert_threat()
        ins_records.insert_plan()
        ins_records.insert_task()
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
        ins_records.insert_version()        
        response = True
    else:
        try:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))            
        except:
            print("migration database record already exist") 
        try: 
            upgrade_db.upgrade_version()
        except:
            print("database upgrade error")                  

    return response   
