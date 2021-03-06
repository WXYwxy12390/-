from sqlalchemy import Column, Integer, String, Float, Boolean, Date, Text, JSON, DateTime

from app.models.base import Base


# 肺功能表
class Lung(Base):
    __tablename__ = 'lung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    detectTime = Column(Date, comment='检测时间')
    FVC_exp = Column(Float, comment='用力肺活量(L)预期值')
    FEV1_FVC_exp = Column(Float, comment='用力呼气一秒率(%)预期值')
    MEF_exp = Column(Float, comment='用力呼气中期流速(L/S)预期值')
    MEF25_exp = Column(Float, comment='25%用力呼气流速(L/S)预期值')
    MEF50_exp = Column(Float, comment='50%用力呼气流速(L/S)预期值')
    MEF75_exp = Column(Float, comment='75%用力呼气流速(L/S)预期值')
    TLC_sb_exp = Column(Float, comment='肺总量(L)预期值')
    RV_exp = Column(Float, comment='残气容积(L)预期值')
    RV_TLC_exp = Column(Float, comment='残气容积/肺总量比(%)预期值')
    VC_exp = Column(Float, comment='肺活量(L)预期值')
    DLCO_ex_exp = Column(Float, comment='无需屏气弥散(mL/mmHg/Mi)预期值')
    DLCO_sb_exp = Column(Float, comment='肺一氧化碳弥散量(mL/mmHg/Mi)预期值')
    KCO_exp = Column(Float, comment='比弥散量预期值')
    FVC_best = Column(Float, comment='用力肺活量(L)最佳值')
    FEV1_FVC_best = Column(Float, comment='用力呼气一秒率(%)最佳值')
    MEF_best = Column(Float, comment='用力呼气中期流速(L/S)最佳值')
    MEF25_best = Column(Float, comment='25%用力呼气流速(L/S)最佳值')
    MEF50_best = Column(Float, comment='50%用力呼气流速(L/S)最佳值')
    MEF75_best = Column(Float, comment='75%用力呼气流速(L/S)最佳值')
    TLC_sb_best = Column(Float, comment='肺总量(L)最佳值')
    RV_best = Column(Float, comment='残气容积(L)最佳值')
    RV_TLC_best = Column(Float, comment='残气容积/肺总量比(%)最佳值')
    VC_best = Column(Float, comment='肺活量(L)最佳值')
    DLCO_ex_best = Column(Float, comment='无需屏气弥散(mL/mmHg/Mi)最佳值')
    DLCO_sb_best = Column(Float, comment='肺一氧化碳弥散量(mL/mmHg/Mi)最佳值')
    KCO_best = Column(Float, comment='比弥散量最佳值')
    FVC_ratio = Column(Float, comment='用力肺活量(L)最佳值/预期值(%)')
    FEV1_FVC_ratio = Column(Float, comment='用力呼气一秒率(%)最佳值/预期值(%)')
    MEF_ratio = Column(Float, comment='用力呼气中期流速(L/S)最佳值/预期值(%)')
    MEF25_ratio = Column(Float, comment='25%用力呼气流速(L/S)最佳值/预期值(%)')
    MEF50_ratio = Column(Float, comment='50%用力呼气流速(L/S)最佳值/预期值(%)')
    MEF75_ratio = Column(Float, comment='75%用力呼气流速(L/S)最佳值/预期值(%)')
    TLC_sb_ratio = Column(Float, comment='肺总量(L)最佳值/预期值(%)')
    RV_ratio = Column(Float, comment='残气容积(L)最佳值/预期值(%)')
    RV_TLC_ratio = Column(Float, comment='残气容积/肺总量比(%)最佳值/预期值(%)')
    VC_ratio = Column(Float, comment='肺活量(L)最佳值/预期值(%)')
    DLCO_ex_ratio = Column(Float, comment='无需屏气弥散(mL/mmHg/Mi)最佳值/预期值(%)')
    DLCO_sb_ratio = Column(Float, comment='肺一氧化碳弥散量(mL/mmHg/Mi)最佳值/预期值(%)')
    KCO_ratio = Column(Float, comment='比弥散量最佳值/预期值(%)')
    FVCMea = Column(Integer, comment='用力肺活量(L)临床意义判定')
    FEV1_FVCMea = Column(Integer, comment='用力呼气一秒率(%)临床意义判定')
    MEFMea = Column(Integer, comment='用力呼气中期流速(L/S)临床意义判定')
    MEF25Mea = Column(Integer, comment='25%用力呼气流速(L/S)临床意义判定')
    MEF50Mea = Column(Integer, comment='50%用力呼气流速(L/S)临床意义判定')
    MEF75Mea = Column(Integer, comment='75%用力呼气流速(L/S)临床意义判定')
    TLC_sbMea = Column(Integer, comment='肺总量(L)临床意义判定')
    RVMea = Column(Integer, comment='残气容积(L)临床意义判定')
    RV_TLCMea = Column(Integer, comment='残气容积/肺总量比(%)临床意义判定')
    VCMea = Column(Integer, comment='肺活量(L)临床意义判定')
    DLCO_exMea = Column(Integer, comment='无需屏气弥散(mL/mmHg/Mi)临床意义判定')
    DLCO_sbMea = Column(Integer, comment='肺一氧化碳弥散量(mL/mmHg/Mi)临床意义判定')
    KCOMea = Column(Integer, comment='比弥散量临床意义判定')
    FVCNote = Column(Text(10000), comment='用力肺活量(L)备注')
    FEV1_FVCNote = Column(Text(10000), comment='用力呼气一秒率(%)备注')
    MEFNote = Column(Text(10000), comment='用力呼气中期流速(L/S)备注')
    MEF25Note = Column(Text(10000), comment='25%用力呼气流速(L/S)备注')
    MEF50Note = Column(Text(10000), comment='50%用力呼气流速(L/S)备注')
    MEF75Note = Column(Text(10000), comment='75%用力呼气流速(L/S)备注')
    TLC_sbNote = Column(Text(10000), comment='肺总量(L)备注')
    RVNote = Column(Text(10000), comment='残气容积(L)备注')
    RV_TLCNote = Column(Text(10000), comment='残气容积/肺总量比(%)备注')
    VCNote = Column(Text(10000), comment='肺活量(L)备注')
    DLCO_exNote = Column(Text(10000), comment='无需屏气弥散(mL/mmHg/Mi)备注')
    DLCO_sbNote = Column(Text(10000), comment='肺一氧化碳弥散量(mL/mmHg/Mi)备注')
    KCONote = Column(Text(10000), comment='比弥散量备注')
    filePath = Column(String(200), comment='文件路径，多个以逗号分隔')

    def keys(self):
        return ['id', 'pid', 'treNum', 'detectTime', 'FVC_exp', 'FEV1_FVC_exp', 'MEF_exp', 'MEF25_exp', 'MEF50_exp',
                'MEF75_exp','TLC_sb_exp', 'RV_exp', 'RV_TLC_exp', 'VC_exp', 'DLCO_ex_exp', 'DLCO_sb_exp', 'KCO_exp', 'FVC_best',
                'FEV1_FVC_best','MEF_best', 'MEF25_best', 'MEF50_best', 'MEF75_best', 'TLC_sb_best', 'RV_best', 'RV_TLC_best',
                'VC_best', 'DLCO_ex_best','DLCO_sb_best', 'KCO_best', 'FVC_ratio', 'FEV1_FVC_ratio', 'MEF_ratio', 'MEF25_ratio', 'MEF50_ratio',
                'MEF75_ratio','TLC_sb_ratio', 'RV_ratio', 'RV_TLC_ratio', 'VC_ratio', 'DLCO_ex_ratio', 'DLCO_sb_ratio', 'KCO_ratio',
                'FVCMea', 'FEV1_FVCMea','MEFMea', 'MEF25Mea', 'MEF50Mea', 'MEF75Mea', 'TLC_sbMea', 'RVMea', 'RV_TLCMea', 'VCMea', 'DLCO_exMea',
                'DLCO_sbMea', 'KCOMea', 'FVCNote','FEV1_FVCNote', 'MEFNote', 'MEF25Note', 'MEF50Note', 'MEF75Note', 'TLC_sbNote',
                'RVNote', 'RV_TLCNote', 'VCNote', 'DLCO_exNote', 'DLCO_sbNote','KCONote','filePath']


# 其他检查表
class OtherExams(Base):
    __tablename__ = 'otherExams'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    ECGDetTime = Column(Date, comment='12导联心电图检测时间')
    ECGDesc = Column(Text, comment='12导联心电图结果描述')  #长度
    ECGPath = Column(String(200), comment='12导联心电图报告路径,多个以逗号分隔')
    UCGDetTime = Column(Date, comment='超声心动图检测时间')
    UCGDesc = Column(Text, comment='超声心动图结果描述')    #长度
    UCGPath = Column(String(200), comment='超声心动图报告路径,多个以逗号分隔')
    def keys(self):
        return ['id','pid','treNum','ECGDetTime','ECGDesc','ECGPath','UCGDetTime','UCGDesc','UCGPath']

# 影像学检查表
class ImageExams(Base):
    __tablename__ = 'ImageExams'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, comment='病人id')
    treNum = Column(Integer, comment='0对应初诊信息、1-n表示对应第x条治疗记录')
    detectTime = Column(Date, comment='检测时间')
    examArea = Column(String(255), comment='检查部位')
    exmaMethod = Column(String(255), comment='检查方法')
    tumorLD = Column(Float, comment='肿瘤长径')
    tumorSD = Column(Float, comment='肿瘤短径')
    tumorDesc = Column(Text, comment='肿瘤描述')
    path = Column(String(200), comment='文件路径,多个以逗号分隔')

    def keys(self):
        return ['id','pid','treNum','detectTime','examArea','exmaMethod','tumorLD','tumorSD','tumorDesc','path']