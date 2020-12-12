class PrescriptionsException(Exception):
    def __init__(self):
        super().__init__()
        self.code = 99
        self.httpstatus = 500
        self.message = "application error"

class MalformedRequestException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 1
        self.httpstatus = 405
        self.message = "malformed request"

class PhysicianNotFoundException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 2
        self.httpstatus = 404
        self.message = "physician not found"

class PatientNotFoundException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 3
        self.httpstatus = 404
        self.message = "patient not found"

class MetricsNotAvailableException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 4
        self.httpstatus = 503
        self.message = "metrics service not available"

class PhysiciansNotAvailableException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 5
        self.httpstatus = 503
        self.message = "physicians service not available"

class PatientsNotAvailableException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 6
        self.httpstatus = 503
        self.message = "patients service not available"

class DatabaseNotAvailableException(PrescriptionsException):
    def __init__(self):
        super().__init__()
        self.code = 7
        self.httpstatus = 503
        self.message = "database service not available"
