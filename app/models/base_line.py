import time

from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime, SmallInteger, and_

from app.models.base import Base, db
# 病人基本信息表
from app.models.cycle import MoleDetec
from app.models.therapy_record import TreRec, OneToFive, Surgery, Radiotherapy
from app.utils.date import get_birth_date_by_id_card, get_age_by_birth, str2date


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='病人id')
    patNumber = Column(String(255), comment='编号')  #长度
    _account = Column(String(40), comment='录入人,多个以逗号分隔,格式为(,17,23,)')
    account = Column(JSON, comment='录入人,多个以逗号分隔,格式为(,17,23,)')

    _researchCenter = Column(String(20), comment='研究中心,多个以逗号分隔,格式为(,17,23,)')
    researchCenter = Column(Integer, comment='研究中心,多个以逗号分隔,格式为(,17,23,)')

    idNumber = Column(String(18), comment='身份证号')
    hospitalNumber = Column(String(255), comment='住院号') #长度
    patientName = Column(String(100), comment='姓名')
    gender = Column(SmallInteger, comment='性别')      #格式问题
    _gender = Column(String(2), comment='性别')  # 格式问题
    birthday = Column(Date, comment='出生日期')
    phoneNumber1 = Column(String(20), comment='电话号码1')  #长度
    phoneNumber2 = Column(String(20), comment='电话号码2')  #长度
    updateTime = Column(DateTime, comment='更新时间')
    nextFollowupTime = Column(DateTime, comment='随访时间')
    finishFollowup = Column(Integer, comment='是否完成随访(True:1、False:0)')

    def keys(self):
        return ['id','patNumber','account','researchCenter','idNumber','hospitalNumber',
                    'patientName','gender','birthday','phoneNumber1','phoneNumber2','updateTime','nextFollowupTime','finishFollowup','update_time',
                    '_researchCenter','_account','_gender']

    def get_fotmat_info(self):
        pat_dia = Patient.get_pat_dia([self.id])
        data = {
            'id':self.id,
            'patNumber':self.patNumber,
            'hospitalNumber':self.hospitalNumber,
            'patientName':self.patientName,
            'idNumber':self.idNumber,
            'phoneNumber':self.phoneNumber1,
            'gender':self.gender,
            'age':get_age_by_birth(get_birth_date_by_id_card(self.idNumber)),
            'patDia': pat_dia[self.id] if pat_dia else None,
            'update_time':self.update_time,
            'research_center_id':self.researchCenter
        }
        return data

    @classmethod
    def search(cls,patients,search_data,page,limit):
        pids = [patient.id for patient in patients]
        #与patient表查询相关的。
        if 'patientName' in search_data or 'patNumber' in search_data \
                or 'idNumber' in search_data or 'hospitalNumber' in search_data or 'gender' in search_data:
            condition = Patient.condition_patient(pids,search_data)
            patients = Patient.query.filter(condition).all()
            pids = [patient.id for patient in patients]
        if 'age1' in search_data and 'age2' in search_data:
            patients = [patient for patient in patients if patient.filter_age(search_data['age1'],search_data['age2'])]
            pids = [patient.id for patient in patients]

        #过滤pdl1，tmb
        if 'PDL1_1' in search_data and 'PDL1_2' in search_data or 'TMB1' in search_data and 'TMB2' in search_data:
            condition = Patient.condition_moleDetec(pids,search_data)
            items = MoleDetec.query.filter(condition).all()
            pids = [item.pid for item in items]

        #治疗方式
        if 'therapy_method' in search_data:
            pids = Patient.filter_theapy_method(pids,search_data['therapy_method'])

        #基因突变位点
        if 'genes' in search_data:
            pids = Patient.filter_genes(pids,search_data['genes'])

        #吸烟，饮酒，激素
        if 'smoke' in search_data or 'drink' in search_data or 'hormone' in search_data:
            condition = Patient.condition_past_his(pids, search_data)
            past_histories = PastHis.query.filter(condition).all()
            pids = [past_history.pid for past_history in past_histories]


        #病理分期
        if 'cliStage' in search_data or 'patStage' in search_data:
            condition = Patient.condition_iniDiaPro(pids, search_data)
            items = IniDiaPro.query.filter(condition).all()
            pids = [item.pid for item in items]

        #病理诊断
        if 'patDia' in search_data:
            pids = Patient.filter_patDia(pids,search_data['patDia'])
        #转移部位 IniDiaPro
        if 'traSite' in search_data:
            pids = Patient.filter_traSite(pids,search_data['traSite'])
        pids = list(set(pids))
        pagination = Patient.query.filter(Patient.is_delete == 0, Patient.id.in_(pids)).order_by(Patient.update_time.desc()).paginate(page=page,per_page=limit)

        return pagination.items,pagination.total

    #获取一组样本中最新的病例诊断
    @classmethod
    def get_pat_dia(cls,pids):
        #把所有的治疗记录拿到，并按照pid进行分组
        tre_recs = TreRec.query.filter(TreRec.is_delete==0,TreRec.pid.in_(pids)).all()

        dict = {}

        for tre_rec in tre_recs:
            if dict.get(tre_rec.pid) is None:
                dict[tre_rec.pid] = []
            dict[tre_rec.pid].append(tre_rec)
        data = {}

        oneToFives = OneToFive.query.filter(OneToFive.is_delete==0,OneToFive.pid.in_(pids)).all()
        surgerys = Surgery.query.filter(Surgery.is_delete==0,Surgery.pid.in_(pids)).all()
        radiotherapys = Radiotherapy.query.filter(Radiotherapy.is_delete==0,Radiotherapy.pid.in_(pids)).all()
        iniDiapros = IniDiaPro.query.filter(IniDiaPro.is_delete==0,IniDiaPro.pid.in_(pids)).all()


        oneToFive_map = Patient.getMap(oneToFives)
        surgery_map = Patient.getMap(surgerys)
        radiotherapy_map = Patient.getMap(radiotherapys)

        iniDiapro_map = {}
        for item in iniDiapros:
            pid = item.pid
            if item and item.patDia and item.patDia.get('radio') != []:
                iniDiapro_map[pid] = item.patDia


        for pid,tre_recs in dict.items():
            tre_recs = sorted(tre_recs,key=lambda tre_rec:tre_rec.treNum,reverse=True)
            for tre_rec in tre_recs:
                trement = tre_rec.trement
                treNum = tre_rec.treNum

                if trement is None:
                    continue
                if trement in ['one','two','three','four','five','other']:
                    if oneToFive_map.get(pid) is None or oneToFive_map[pid].get(tre_rec.treNum) is None:
                        continue
                    item = oneToFive_map.get(pid).get(treNum)
                    if item and item.patDia and item.patDia.get('radio') != []:
                        data[pid] = item.patDia
                        break
                elif trement == 'surgery':
                    if surgery_map.get(pid) is None or surgery_map[pid].get(tre_rec.treNum) is None:
                        continue
                    item = surgery_map[pid][tre_rec.treNum]
                    if item and item.patDia and item.patDia.get('radio') != []:
                        data[pid] = item.patDia
                        break
                elif trement == 'radiotherapy':
                    if radiotherapy_map.get(pid) is None or radiotherapy_map[pid].get(tre_rec.treNum) is None:
                        continue
                    item = radiotherapy_map[pid][tre_rec.treNum]
                    if item and item.patDia and item.patDia.get('radio') != []:
                        data[pid] = item.patDia
                        break
        for pid,item in iniDiapro_map.items():
            if pid not in data:
                data[pid] = iniDiapro_map.get(pid)
        return data if data != {} else None

    @classmethod
    def getMap(cls,model_items):
        dict = {}
        for model_item in model_items:
            pid = model_item.pid
            if dict.get(pid) is None:
                dict[pid] = {}
            dict[pid][model_item.treNum] = model_item
        return dict

    @staticmethod
    def condition_patient(pids, data):

        # 这里必须用and_连起来两个条件，否则会被当作元组
        condtion = and_(Patient.is_delete == 0, Patient.id.in_(pids))
        if 'patientName' in data:
            condtion = and_(condtion, Patient.patientName.like('%' + data['patientName'] + '%'))
        if 'patNumber' in data:
            condtion = and_(condtion, Patient.patNumber.like(data['patNumber'] + '%'))
        if 'idNumber' in data:
            condtion = and_(condtion,Patient.idNumber.like(data['idNumber'] + '%'))
        if 'hospitalNumber' in data:
            condtion = and_(condtion,Patient.hospitalNumber.like(data['hospitalNumber'] + '%'))
        if 'gender' in data:
            condtion = and_(condtion, Patient.gender == data['gender'])

        return condtion

    @staticmethod
    def condition_past_his(pids,data):

        condtion = and_(PastHis.is_delete == 0, PastHis.pid.in_(pids))
        if 'smoke' in data:
            condtion = and_(condtion, PastHis.smoke == data['smoke'])
        if 'drink' in data:
            condtion = and_(condtion, PastHis.drink == data['drink'])
        if 'hormone' in data:
            condtion = and_(condtion, PastHis.hormone == data['hormone'])
        return condtion

    @staticmethod
    def condition_iniDiaPro(pids,data):

        condtion = and_(IniDiaPro.is_delete == 0,IniDiaPro.pid.in_(pids))
        if 'patStage' in data:
            condtion = and_(condtion, IniDiaPro.patStage == data['patStage'])
        if 'cliStage' in data:
            condtion = and_(condtion, IniDiaPro.cliStage == data['cliStage'])
        return condtion

    @staticmethod
    def condition_moleDetec(pids,search_data):
        condtion = and_(MoleDetec.is_delete==0,MoleDetec.pid.in_(pids))
        if 'PDL1_1' in search_data and 'PDL1_2' in search_data:
            condtion = and_(condtion, MoleDetec.PDL1 >= search_data['PDL1_1'],MoleDetec.PDL1 <= search_data['PDL1_2'])
        if 'TMB1' in search_data and 'TMB2' in search_data:
            condtion = and_(condtion,MoleDetec.TMB >= search_data['TMB1'], MoleDetec.TMB <= search_data['TMB2'])

        return condtion



    #过滤基因突变
    @classmethod
    def filter_genes(cls,pids,genes):
        mole_detecs = MoleDetec.query.filter(MoleDetec.is_delete == 0, MoleDetec.pid.in_(pids)).all()
        mole_detec_map = {}
        for mole_detec in mole_detecs:
            pid = mole_detec.pid
            if mole_detec_map.get(pid) is None:
                mole_detec_map[pid] = []
            mole_detec_map[pid].append(mole_detec)

        res = []
        for pid,mole_detecs in mole_detec_map.items():
            gene_record = set()
            for mole_detec in mole_detecs:
                if mole_detec.ALK == 1:
                    gene_record.add('ALK')
                if mole_detec.BIM == 1:
                    gene_record.add('BIM')
                if mole_detec.BRAF == 1:
                    gene_record.add('BRAF')
                if mole_detec.cMET == 1:
                    gene_record.add('cMET')
                if mole_detec.EGFR == 1:
                    gene_record.add('EGFR')
                if mole_detec.HER_2 == 1:
                    gene_record.add('HER_2')
                if mole_detec.KRAS == 1:
                    gene_record.add('KRAS')
                if mole_detec.PIK3CA == 1:
                    gene_record.add('PIK3CA')
                if mole_detec.ROS1 == 1:
                    gene_record.add('ROS1')
                if mole_detec.RET == 1:
                    gene_record.add('RET')
                if mole_detec.UGT1A1 == 1:
                    gene_record.add('UGT1A1')
                if len(gene_record) == 11:
                    break
            gene_record = list(gene_record) #去重
            flag = True
            for gene in genes:
                if gene not in gene_record:
                    flag = False
                    break
            if flag:
                res.append(pid)
        return res

    def filter_age(self,age1,age2):
        if self.idNumber is None or self.idNumber == "":
            return None
        birth = get_birth_date_by_id_card(self.idNumber)
        age = get_age_by_birth(birth)
        if age is None or age < age1 or age > age2:
            return None
        return self

    # @classmethod
    # def filter_PDL(cls,pids,PDL_val1,PDL_val2):
    #     mole_detecs = MoleDetec.query.filter(MoleDetec.is_delete==0,MoleDetec.pid.in_(pids),
    #                                          MoleDetec.PDL1 >= PDL_val1,MoleDetec.PDL1 <= PDL_val2).all()
    #     data = [mole_detec.pid for mole_detec in mole_detecs]
    #     return data
    # @classmethod
    # def filter_TMB(cls,pids,TMB1,TMB2):
    #     mole_detecs = MoleDetec.query.filter(MoleDetec.is_delete == 0, MoleDetec.pid.in_(pids),
    #                                          MoleDetec.TMB >= TMB1, MoleDetec.TMB <= TMB2).all()
    #     data = [mole_detec.pid for mole_detec in mole_detecs]
    #     return data

    @classmethod
    def filter_theapy_method(cls,pids,method):
        trement = method.get('trement')
        treSolu = method.get('treSolu')

        if trement:
            tre_recs = TreRec.query.filter(TreRec.is_delete == 0,TreRec.pid.in_(pids), TreRec.trement == trement).all()
            pids = [tre_rec.pid for tre_rec in tre_recs]
        if treSolu is None:
            return pids

        #只有1-5线，和其他，中有详细治疗。
        items = OneToFive.query.filter(OneToFive.is_delete==0,OneToFive.pid.in_(pids)).all()
        tre_rec_map = {}
        for item in items:
            if item.treSolu is None:
                continue
            pid = item.pid
            if tre_rec_map.get(pid) is None:
                tre_rec_map[pid] = []
            tre_rec_map[pid].extend(item.treSolu.split(','))
        res = []
        for pid,treSolus in tre_rec_map.items():
            if treSolu in treSolus:
                res.append(pid)

        return list(set(res))

    @classmethod
    def filter_patDia(cls,pids,items):

        pat_dia = Patient.get_pat_dia(pids)
        data = []
        for pid,pat_dia in pat_dia.items():
            flag = True
            radio = pat_dia.get('radio')
            if radio is None or radio == []:
                continue
            for item in items:
                is_start = False
                for radio_item in radio:
                    if radio_item.startswith(item):
                        is_start = True
                if is_start == False:
                    flag = False
                    break
            if flag:
                data.append(pid)
        return data

    @classmethod
    def filter_traSite(cls, pids, items):

        ini_dia_pros = IniDiaPro.query.filter(IniDiaPro.pid.in_(pids)).all()

        patient_ids = []
        for ini_dia_pro in ini_dia_pros:
            if ini_dia_pro.traSite is None:
                continue
            radio = ini_dia_pro.traSite.get('radio')
            flag = True
            for item in items:
                if item not in radio:
                    flag = False
                    break
            if flag:
                patient_ids.append(ini_dia_pro.pid)

        return patient_ids


# 病人既往史表
class PastHis(Base):
    __tablename__ = 'pastHis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')

    basDisHis = Column(JSON, comment='基础疾病史,多个以逗号分隔')
    _basDisHis = Column(String(100), comment='基础疾病史,多个以逗号分隔')  #长度

    infDisHis = Column(JSON, comment='传染疾病史,多个以逗号分隔')
    _infDisHis = Column(String(100), comment='传染疾病史,多个以逗号分隔')  #长度

    tumor = Column(Boolean, comment='肿瘤史（无、有）')

    tumHis = Column(JSON, comment='肿瘤史,多个以逗号分隔')  # 长度
    _tumHis = Column(String(100), comment='肿瘤史,多个以逗号分隔')        #长度

    tumorFam = Column(Boolean, comment='肿瘤家族史（无、有）')

    tumFamHis = Column(JSON, comment='肿瘤家族史,多个以逗号分隔')
    _tumFamHis = Column(String(100), comment='肿瘤家族史,多个以逗号分隔')  #长度

    smoke = Column(Boolean, comment='是否吸烟')
    smokingHis = Column(JSON, comment='吸烟史, {stopSmoke: 是否戒烟, smokeDayAvg: 日平均吸烟量/支, smokeYearAvg: 累计吸烟时间/年,stopSmokeHis: 戒烟时间}')
    drink = Column(Boolean, comment='是否饮酒（否、是）')
    drinkingHis = Column(JSON, comment='饮酒史, {stopDrink: 是否戒酒, drinkDayAvg: 日平均饮酒量, drinkYearAvg: 累计饮酒时间/年,stopDrinkHis: 戒酒时间}')
    hormone = Column(Boolean, comment='是否长期使用激素')
    hormoneUseHis = Column(JSON, comment='激素使用史,[{key: , drugDose: 2g, drugName: 药物1, duration: 1}, {key: 1, drugDose: 1g, drugName: 药物2, duration: 2}]')
    drug = Column(Boolean, comment='是否长期使用药物')
    drugUseHis = Column(JSON, comment='药物使用史,[{key: , drugDose: 2g, drugName: 药物1, duration: 1}, {key: 1, drugDose: 1g, drugName: 药物2, duration: 2}]')

    def keys(self):
        return ['id','pid','basDisHis','infDisHis','tumor','tumHis','tumorFam','tumFamHis','smoke','smokingHis',
                'drink','drinkingHis','hormone','hormoneUseHis','drug','drugUseHis','_basDisHis','_tumHis','_tumFamHis']

#激素史与药物史
class DrugHistory(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    type = Column(SmallInteger,comment='type=1,激素史，type = 0，其他药物史')
    drug_name = Column(String(255))
    drug_dose = Column(String(255))
    use_time = Column(Float)

    def keys(self):
        return ['id','drug_name','drug_dose','use_time']







# 病人初诊过程信息表
class IniDiaPro(Base):
    __tablename__ = 'iniDiaPro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id',index=True)
    PSScore = Column(Integer, comment='首诊PS评分0-4')

    cliniManifest = Column(JSON, comment='临床表现,多个以逗号分隔')  # 长度
    _cliniManifest = Column(String(40), comment='临床表现,多个以逗号分隔')  #长度

    videography = Column(Boolean, comment='影像学 0-周围型；1-中央型')

    part = Column(JSON, comment='部位,多个以逗号分隔')
    _part = Column(String(100), comment='部位,多个以逗号分隔')

    bioMet = Column(JSON, comment='活检方式,多个以逗号分隔')  # 长度
    _bioMet = Column(String(40), comment='活检方式,多个以逗号分隔') #长度

    pleInv = Column(Boolean, comment='是否胸膜侵犯')
    speSite = Column(String(255), comment='标本部位')
    firVisDate = Column(Date, comment='初诊日期')
    patReDate = Column(Date, comment='病理报告日期')
    patNum = Column(String(255), comment='病理号') # 改为字符串

    patDia = Column(JSON, comment='病理诊断,多个以逗号分隔')
    _patDia = Column(String(10000), comment='病理诊断,多个以逗号分隔')
    _patDiaOthers = Column(String(255), comment='病理诊断,其他的内容')

    mitIma = Column(String(255), comment='核分裂像')
    comCar = Column(String(255), comment='复合性癌') #长度
    necArea = Column(Float, comment='坏死面积')
    massSize = Column(String(255), comment='肿块大小')
    Ki67 = Column(Float, comment='Ki67')

    traSite = Column(JSON, comment='转移部位')  #长度
    _traSite = Column(String(100), comment='转移部位')  # 长度

    TSize = Column(String(255), comment='TSize')           #文本
    stage = Column(String(30), comment='分期情况')    #格式问题
    cStage = Column(JSON, comment='c分期TNM,以逗号分隔,格式为(1,2,3或1,,2)')
    cliStage = Column(String(30), comment='临床分期')
    pStage = Column(JSON, comment='p分期TNM,以逗号分隔,格式为(1,2,3或1,,2)')
    patStage = Column(String(30), comment='病理分期')
    cRemark = Column(Text(10000))
    pRemark = Column(Text(10000))

    def keys(self):
        return ["id","PSScore","cliniManifest","videography","part","bioMet","pleInv","speSite","firVisDate",
                "patReDate","patNum","patDia","mitIma","comCar","necArea","massSize","Ki67",
                "traSite","TSize","stage","cStage","cliStage","pStage","patStage",'cRemark','pRemark',
                '_cliniManifest','_part','_bioMet','_traSite','_patDia','_patDiaOthers']