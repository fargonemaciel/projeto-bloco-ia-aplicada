from typing import Literal
from pydantic import BaseModel, Field, field_validator


class TextoParaResumo(BaseModel):
    texto: str = Field(
        ...,
        min_length=50,
        max_length=10_000,
        description="Texto em português que será resumido pelo modelo local.",
    )

    @field_validator("texto")
    @classmethod
    def validar_texto(cls, texto):
        texto_limpo = texto.strip()
        if len(texto_limpo) < 50:
            raise ValueError("O texto deve possuir pelo menos 50 caracteres úteis.")
        return texto_limpo


class ResumoResposta(BaseModel):
    tipo_analise: Literal["resumo"] = "resumo"
    modelo: str
    resumo: str
    caracteres_entrada: int = Field(ge=1)
    tokens_entrada: int = Field(ge=1)
    tokens_processados: int = Field(ge=1)
    texto_truncado: bool
    tempo_inferencia_segundos: float = Field(ge=0)
    execucao: Literal["local"] = "local"
