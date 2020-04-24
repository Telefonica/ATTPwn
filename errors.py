class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class WarriorAlreadyExistsError(Exception):
    pass

class UpdatingWarriorError(Exception):
    pass

class DeletingWarriorError(Exception):
    pass

class WarriorNotExistsError(Exception):
    pass

class PlanAlreadyExistsError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "WarriorAlreadyExistsError": {
         "message": "Warrior with given name already exists",
         "status": 400
     },
     "UpdatingWarriorError": {
         "message": "Updating Warrior added by other is forbidden",
         "status": 403
     },
     "DeletingWarriorError": {
         "message": "Deleting Warrior added by other is forbidden",
         "status": 403
     },
     "WarriorNotExistsError": {
         "message": "Warrior with given id doesn't exists",
         "status": 400
     },
     "PlanAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     }
}