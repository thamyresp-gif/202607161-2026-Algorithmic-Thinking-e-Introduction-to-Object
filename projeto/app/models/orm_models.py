from .database import db


class ImovelORM(db.Model):
    __tablename__ = "imovel"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    endereco = db.Column(db.String(255))
    quartos = db.Column(db.Integer)
    vagas_garagem = db.Column(db.Integer)


class OrcamentoORM(db.Model):
    __tablename__ = "orcamento"
    id = db.Column(db.Integer, primary_key=True)
    imovel_id = db.Column(db.Integer, db.ForeignKey("imovel.id"), nullable=False)
    tem_filhos = db.Column(db.Boolean, default=False)
    parcelar = db.Column(db.Boolean, default=False)
    num_parcelas = db.Column(db.Integer)
    aluguel_base = db.Column(db.Float)
    valor_acrescimos = db.Column(db.Float, default=0)
    valor_desconto = db.Column(db.Float, default=0)
    valor_garagem = db.Column(db.Float, default=0)
    taxa_contrato = db.Column(db.Float, default=0)
    valor_total_mensal = db.Column(db.Float)
    parcela_contrato = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default="A_VISTA")
    criado_em = db.Column(db.DateTime, server_default=db.func.now())


class ParcelaORM(db.Model):
    __tablename__ = "parcela"
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey("orcamento.id"), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Float, nullable=False)