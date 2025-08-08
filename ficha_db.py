from sqlalchemy import create_engine, Column, String, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base

# Criar db
db_rpg = create_engine("sqlite:///Ficha.db")  # tipo de sql:///nome do db.db

# Sessão com o db
Session = sessionmaker(bind=db_rpg)
session = Session()

Base = declarative_base()  # permitir herança de classes


class Ficha(Base):
    __tablename__ = 'Fichas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_personagem = Column('nome do personagem', String)
    hp_total = Column('hp total', Integer)
    hp_atual = Column('hp atual', Integer)
    vivo = Column('vida', Boolean)
    level = Column('level', Integer)
    xp = Column('xp', Integer)
    armour_hp = Column('vida extra da armadura', Integer)
    armadura = Column('armadura', Integer)
    mare = Column('resistencia magica', Integer)  # resistência mágica
    classe_armadura = Column('quanto que o inimigo precisa acertar', Integer)
    movimento_padrao = Column('movimento padrao', Integer)
    movimento_total = Column('movimento total', Integer)
    esquiva_padrao = Column('esquiva padrao', Integer)
    esquiva_total = Column('esquiva total', Integer)
    dinheiro = Column('dinheiro', Integer)
    mana_atual = Column('mana atual(esp)', Integer)
    mana_max = Column('mana maxima(esp max)', Integer)
    hab_principal = Column('habilidade principal', String)
    hab_principal_qnt_uso = Column('quantidade de usos da habilidade principal', Integer)
    hab_principal_qnt_usada = Column('quantidade de usada da habilidade principal', Integer)
    hab_bonus = Column('habilidade bonus', String)
    hab_bonus_qnt_uso = Column('quantidade de usos da habilidade bonus', Integer)
    hab_bonus_qnt_usada = Column('quantidade de usos da habilidade bonus', Integer)
    passiva = Column('passiva', String)

    def __init__(self, nome_personagem, hp_total, hp_atual, vivo, level, xp, armour_hp,
                 armadura, mare, classe_armadura, movimento_padrao,
                 movimento_total, esquiva_padrao, esquiva_total, dinheiro,
                 mana_atual, mana_max, hab_principal, hab_principal_qnt_uso,
                 hab_principal_qnt_usada, hab_bonus, hab_bonus_qnt_uso,
                 hab_bonus_qnt_usada, passiva):

        self.nome_personagem = nome_personagem
        self.hp_total = hp_total
        self.hp_atual = hp_atual
        self.vivo = vivo
        self.level = level
        self.xp = xp
        self.armour_hp = armour_hp
        self.armadura = armadura
        self.mare = mare
        self.classe_armadura = classe_armadura
        self.movimento_padrao = movimento_padrao
        self.movimento_total = movimento_total
        self.esquiva_padrao = esquiva_padrao
        self.esquiva_total = esquiva_total
        self.dinheiro = dinheiro
        self.mana_atual = mana_atual
        self.mana_max = mana_max
        self.hab_principal = hab_principal
        self.hab_principal_qnt_uso = hab_principal_qnt_uso
        self.hab_principal_qnt_usada = hab_principal_qnt_usada
        self.hab_bonus = hab_bonus
        self.hab_bonus_qnt_uso = hab_bonus_qnt_uso
        self.hab_bonus_qnt_usada = hab_bonus_qnt_usada
        self.passiva = passiva


# Criar o banco de dados
Base.metadata.create_all(bind=db_rpg)