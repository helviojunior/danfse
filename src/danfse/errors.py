"""Exceções da biblioteca danfse."""


class DanfseError(Exception):
    """Erro base da biblioteca."""


class XmlInvalidoError(DanfseError):
    """O conteúdo informado não é um XML de NFS-e Nacional válido."""


class CampoObrigatorioError(DanfseError):
    """Um campo obrigatório para montar a DANFSe não foi encontrado no XML."""
