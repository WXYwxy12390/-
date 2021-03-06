from flask import request, g

from app.libs.decorator import edit_need_auth
from app.libs.error import Success
from app.libs.error_code import ParameterException
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models import json2db
from app.models.base_line import Patient
from app.spider.user_info import UserInfo

api = Redprint('patient')

@api.route('/<int:id>',methods = ['GET'])
def get_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    return Success(data=patient if patient else {})


@api.route('/<int:pid>',methods = ['POST'])
@auth.login_required
@edit_need_auth
def add_patient(pid):
    data = request.get_json()
    patient = Patient.query.get_or_404(pid)
    if 'idNumber' in data:
        item = Patient.query.filter(Patient.is_delete == 0, Patient.idNumber == data['idNumber'],
                                       Patient.id != pid, Patient.researchCenter == patient.researchCenter).first()
        if item:
            raise ParameterException(msg='已经存在相同身份证号码。')
    if 'hospitalNumber' in data and patient.hospitalNumber is not None:
        item = Patient.query.filter(Patient.is_delete == 0, Patient.hospitalNumber == data['hospitalNumber'],
                                       Patient.id != pid, Patient.researchCenter == patient.researchCenter).first()
        if item:
            raise ParameterException(msg='已经存在相同住院号。')
    json2db(data, Patient)
    return Success()