# app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    JSON,
    ARRAY,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base

# Remove this line as Base is now imported from base.py
# Base = declarative_base()

class Activacion(Base):
    __tablename__ = 'activacion'

    id_lote = Column(Integer, primary_key=True, autoincrement=True)
    usuario_activador = Column(String(100), nullable=False)
    fecha_activacion = Column(Date, nullable=False)
    numero_archivos = Column(Integer, nullable=False)

    index_table = relationship("IndexTable", back_populates="activacion")
    documentos_generados = relationship("DocumentosGenerados", back_populates="activacion")


class IndexTable(Base):
    __tablename__ = 'index_table'

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    id_lote = Column(Integer, ForeignKey('activacion.id_lote'), nullable=False)
    titulo_documento = Column(String(255), nullable=False)
    ocr = Column(Boolean, default=False)
    tipo_documento = Column(String(100), nullable=False)
    trasladado_descargados = Column(Boolean, default=False)
    url_descargados = Column(String(255), nullable=True)
    usuario_dueno = Column(String(100), nullable=False)
    supervisado = Column(Boolean, default=False)

    activacion = relationship("Activacion", back_populates="index_table")
    documento = relationship("Documento", uselist=False, back_populates="index_table")
    contrato = relationship("Contratos", uselist=False, back_populates="index_table")
    otrosi = relationship("Otrosi", uselist=False, back_populates="index_table")
    poliza = relationship("Poliza", uselist=False, back_populates="index_table")


class Documento(Base):
    __tablename__ = 'documento'

    id_documento = Column(Integer, ForeignKey('index_table.id_documento'), primary_key=True)
    id_lote = Column(Integer, ForeignKey('activacion.id_lote'), nullable=False)
    contenido = Column(String, nullable=False)

    index_table = relationship("IndexTable", back_populates="documento")


class Contratos(Base):
    __tablename__ = 'contratos'

    id_documento = Column(Integer, ForeignKey('index_table.id_documento'), primary_key=True)
    id_lote = Column(Integer, ForeignKey('activacion.id_lote'), nullable=False)
    consecutivo_contrato = Column(String(100), nullable=False)
    programa_mitigacion = Column(String(255), nullable=False)
    json_contratos_info_general = Column(JSON, nullable=False)
    json_contratos_clausulas = Column(JSON, nullable=False)
    json_contratos_amparos = Column(JSON, nullable=False)

    index_table = relationship("IndexTable", back_populates="contrato")
    tabla_madre = relationship("TablaMadre", back_populates="contrato", uselist=False)


class Otrosi(Base):
    __tablename__ = 'otrosi'

    id_documento = Column(Integer, ForeignKey('index_table.id_documento'), primary_key=True)
    id_lote = Column(Integer, ForeignKey('activacion.id_lote'), nullable=False)
    numero_otrosi = Column(String(100), nullable=False)
    consecutivo_contrato = Column(String(100), nullable=False)
    json_otrosi_info_general = Column(JSON, nullable=False)
    json_otrosi_modificaciones = Column(JSON, nullable=False)

    index_table = relationship("IndexTable", back_populates="otrosi")
    tabla_madre = relationship("TablaMadre", secondary="otrosi_tabla_madre", back_populates="otrosi")


class Poliza(Base):
    __tablename__ = 'poliza'

    id_documento = Column(Integer, ForeignKey('index_table.id_documento'), primary_key=True)
    id_lote = Column(Integer, ForeignKey('activacion.id_lote'), nullable=False)
    numero_otrosi = Column(String(100), nullable=True)
    numero_poliza = Column(String(100), nullable=False)
    consecutivo_contrato = Column(String(100), nullable=False)
    json_poliza_info_general = Column(JSON, nullable=False)
    json_poliza_amparos = Column(JSON, nullable=False)
    hallazgos = Column(Boolean, default=False)

    index_table = relationship("IndexTable", back_populates="poliza")
    tabla_madre = relationship("TablaMadre", secondary="poliza_tabla_madre", back_populates="poliza")


class DocumentosGenerados(Base):
    __tablename__ = 'documentos_generados'

    id_documento_generado = Column(Integer, primary_key=True, autoincrement=True)
    id_lote = Column(Integer, ForeignKey('activacion.id_lote'), nullable=False)
    consecutivo_contrato = Column(String(100), nullable=False)
    titulo_documento_generado = Column(String(255), nullable=False)
    url_documento_generado = Column(String(255), nullable=False)
    json_total = Column(JSON, nullable=False)
    enviado = Column(Boolean, default=False)

    activacion = relationship("Activacion", back_populates="documentos_generados")


class TablaMadre(Base):
    __tablename__ = 'tabla_madre'

    consecutivo_contrato = Column(String(100), primary_key=True)
    id_documento_contrato = Column(Integer, ForeignKey('contratos.id_documento'), nullable=False)
    id_documento_otrosi = Column(ARRAY(Integer))
    id_documento_poliza = Column(ARRAY(Integer))
    done = Column(Boolean)
    query = Column(Integer, nullable=False)

    contrato = relationship("Contratos", back_populates="tabla_madre")
    otrosi = relationship("Otrosi", secondary="otrosi_tabla_madre", back_populates="tabla_madre")
    poliza = relationship("Poliza", secondary="poliza_tabla_madre", back_populates="tabla_madre")


class OtrosiTablaMadre(Base):
    __tablename__ = "otrosi_tabla_madre"

    id_documento = Column(Integer, ForeignKey('otrosi.id_documento'), primary_key=True)
    consecutivo_contrato = Column(String(100), ForeignKey('tabla_madre.consecutivo_contrato'), primary_key=True)


class PolizaTablaMadre(Base):
    __tablename__ = "poliza_tabla_madre"

    id_documento = Column(Integer, ForeignKey('poliza.id_documento'), primary_key=True)
    consecutivo_contrato = Column(String(100), ForeignKey('tabla_madre.consecutivo_contrato'), primary_key=True)

# Define other chain tables and supervisor chain tables similarly
# For brevity, they are not fully defined here
