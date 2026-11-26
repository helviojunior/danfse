# Changelog

Todas as mudanças relevantes deste projeto são documentadas aqui.
O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Unreleased]

## [0.1.0] - 2026-11-25

### Adicionado

- Geração da DANFSe (NFS-e Nacional, leiaute v2.0) em PDF a partir do XML.
- API: `generate`, `generate_from_file`, `generate_from_string` e `Options`.
- CLI `danfse` (`danfse nota.xml -o saida.pdf`).
- Renderização HTML + CSS via WeasyPrint; QR Code de consulta pública (segno).
- Parser defensivo do XML (agnóstico a namespace), lookup de municípios (IBGE),
  formatadores pt-BR (CNPJ/CPF/CEP/moeda/datas) e rótulos do leiaute.
- Marca d'água (cancelada / substituída / homologação) e rodapé configurável.

[Unreleased]: https://github.com/helviojunior/danfse/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/helviojunior/danfse/releases/tag/v0.1.0
