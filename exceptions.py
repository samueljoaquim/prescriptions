class PrescriptionsException(Exception):
    pass

class MalformedRequestException(PrescriptionsException):
    def __init__(self):
        self.code = 1
        self.httpstatus = 400
        self.message = "malformed request"

class PhysicianNotFoundException(PrescriptionsException):
    def __init__(self):
        self.code = 2
        self.httpstatus = 404
        self.message = "physician not found"

class PatientNotFoundException(PrescriptionsException):
    def __init__(self):
        self.code = 3
        self.httpstatus = 404
        self.message = "patient not found"

class MetricsNotAvailableException(PrescriptionsException):
    def __init__(self):
        self.code = 4
        self.httpstatus = 503
        self.message = "metrics service not available"

class PhysiciansNotAvailableException(PrescriptionsException):
    def __init__(self):
        self.code = 5
        self.httpstatus = 503
        self.message = "physicians service not available"

class PatientsNotAvailableException(PrescriptionsException):
    def __init__(self):
        self.code = 6
        self.httpstatus = 503
        self.message = "patients service not available"