import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, PrimaryKeyConstraint, ForeignKey, \
    Boolean, DateTime, UniqueConstraint

pd.options.display.max_columns = None
pd.options.display.max_rows = None
Base = declarative_base()


class Customer(Base):
    __tablename__ = "CustomerProfile"
    SNo = Column(Integer, primary_key=True)
    ClientID = Column(String)
    ClientName = Column(String)
    APIKey = Column(String)
    SecretKey = Column(String)
    OrgCap = Column(Float)
    CashCap = Column(Float)
    FutCap = Column(Float)
    TradeCash = Column(Float)
    TradeFut = Column(Float)
    MaxEntryCapital = Column(Float)
    CashTrade = Column(Boolean)
    FutTrade = Column(Boolean)


class Stock(Base):
    __tablename__ = "StockProfile"
    SNo = Column(Integer, primary_key=True)
    Symbol = Column(String)
    Segment = Column(String)
    ExchID = Column(Integer)
    Lot = Column(String)
    TotalMargin = Column(Float)
    ContractMon = Column(String)


class NinjaCalls(Base):
    __tablename__ = "NinjaCalls"
    SNo = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(String)
    Symbol = Column(String)
    Segment = Column(String)
    CallType = Column(String)
    Rate = Column(Float)
    SL = Column(Float)
    TGT = Column(Float)
    Closure = Column(String)
    ExitAt = Column(String)
    SquareOffRate = Column(Float)
    EntryAt = Column(String)
    OrderPlacement = Column(String)
    QTY = Column(Integer)
    PL = Column(Float)


class RecoCalls(Base):
    __tablename__ = "RecCalls"
    SNo = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(String)
    Symbol = Column(String)
    Segment = Column(String)
    EntryAt = Column(String)
    CallType = Column(String)
    Rate = Column(Float)
    QTY = Column(Integer)
    TGT = Column(Float)
    SL = Column(Float)
    RecoState = Column(Integer)
    Cycle = Column(Integer)
    UniqueConstraint(Symbol, Date, name="uix_1")


class RecoCallsClosure(Base):
    __tablename__ = "RecClosure"
    SNo = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(String)
    Symbol = Column(String)
    Segment = Column(String)
    EntryAt = Column(String)
    ExitAt = Column(String)
    CallType = Column(String)
    Rate = Column(Float)
    QTY = Column(Integer)
    TGT = Column(Float)
    SL = Column(Float)
    Closure = Column(String)
    RecoState = Column(Integer)
    SquareOffRate = Column(String)
    Cycle = Column(Integer)
    UniqueConstraint(Symbol, Date, name="uix_1")


class Transaction(Base):
    __tablename__ = "Transactions"
    SNo = Column(Integer, primary_key=True)
    Date = Column(String)
    ClientID = Column(Integer)
    ClientName = Column(String)
    Symbol = Column(String)
    Segment = Column(String)
    EntryAt = Column(String)
    ExitAt = Column(String)
    CallType = Column(String)
    Rate = Column(Float)
    TradedRate = Column(Float)
    QTY = Column(Integer)
    TGT = Column(Float)
    SL = Column(Float)
    SquareOffRate = Column(Float)
    CapitalAvailable = Column(Float)
    CapitalUsed = Column(Float)
    OrderID = Column(String)
    TgtID = Column(String)
    SlID = Column(String)
    OrderStatus = Column(String)
    TgtStatus = Column(String)
    SlStatus = Column(String)
    Through = Column(String)


class DBManager(object):
    __shared_instance = 'DBManager'

    @staticmethod
    def instance():
        if DBManager.__shared_instance == 'DBManager':
            DBManager()
        return DBManager.__shared_instance

    def __init__(self):
        if DBManager.__shared_instance != 'DBManager':
            raise Exception("This class is a singleton class !")
        else:
            self.create_engine()
            self.register_tables()
            DBManager.__shared_instance = self

    def create_engine(self):
        self.engine = create_engine('Data/DBEngine.db')
        self.register_tables()
        self.create_session()

    def register_tables(self):
        Customer.__table__.create(bind=self.engine, checkfirst=True)
        Stock.__table__.create(bind=self.engine, checkfirst=True)
        NinjaCalls.__table__.create(bind=self.engine, checkfirst=True)
        RecoCalls.__table__.create(bind=self.engine, checkfirst=True)
        RecoCallsClosure.__table__.create(bind=self.engine, checkfirst=True)
        Transaction.__table__.create(bind=self.engine, checkfirst=True)

    def get_engine(self):
        return self.engine

    def create_session(self):
        Session = sessionmaker(bind=self.get_engine())
        self.session = Session()

    def get_session(self):
        return self.session


class DB(object):
    dbm = None

    def __init__(self):
        self.dbm = DBManager.instance()

    def get_engine(self):
        return self.dbm.get_engine()

    def get_session(self):
        return self.dbm.get_session()


class CustomerManager(DB):
    def __init__(self):
        super(CustomerManager, self).__init__()

    # print(self.dbm.get_session())

    def get_all_customers(self):
        result1 = self.dbm.get_session().query(Customer).all()
        return result1


class StockManager(DB):
    def __init__(self):
        super(StockManager, self).__init__()

    def get_all_customers(self):
        result1 = self.dbm.get_session().query(Stock).all()
        return result1


class NinjaManager(DB):
    def __init__(self):
        super(NinjaManager, self).__init__()

    def get_all_customers(self):
        result1 = self.dbm.get_session().query(NinjaCalls).all()
        return result1


class RecoCallManager(DB):
    def __init__(self):
        super(RecoCallManager, self).__init__()

    def get_all_customers(self):
        result1 = self.dbm.get_session().query(RecoCalls).all()
        return result1


class RecoClosureManager(DB):
    def __init__(self):
        super(RecoClosureManager, self).__init__()

    def get_all_customers(self):
        result1 = self.dbm.get_session().query(RecoCallsClosure).all()
        return result1


class TransactionManager(DB):
    def __init__(self):
        super(TransactionManager, self).__init__()

    def get_all_customers(self):
        result1 = self.dbm.get_session().query(Transaction).all()
        return result1


if __name__ == "__main__":
    cm = CustomerManager()
    sm = StockManager()
    nm = NinjaManager()
    cr = RecoCallManager()
    cc = RecoClosureManager()
    tm = TransactionManager()

    # q = tm.get_session().query(Customer).filter(Customer.txns.has(Transaction.tgt_status == 'Open'))
    # df = pd.read_sql(q.statement,tm.get_session().bind)
    # print(df.shape)
    # print(df)

    # q = tm.get_session().query(Transaction)
    # q = q.where((Transaction.tgt_status == "Open"))

# tm.create_engine()
# print(tm.get_engin())
