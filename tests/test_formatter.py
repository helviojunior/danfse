from danfse import formatter as fmt


def test_cnpj():
    assert fmt.cnpj_cpf("40569411000117") == "40.569.411/0001-17"


def test_cpf():
    assert fmt.cnpj_cpf("12345678909") == "123.456.789-09"


def test_cep():
    assert fmt.cep("30240300") == "30240-300"


def test_currency():
    assert fmt.currency("117.60") == "R$ 117,60"
    assert fmt.currency("1234567.8") == "R$ 1.234.567,80"
    assert fmt.currency("") == "-"


def test_date_and_datetime():
    assert fmt.date("2026-04-13") == "13/04/2026"
    assert fmt.date_time("2026-04-13T11:28:02-03:00") == "13/04/2026 11:28:02"


def test_cod_trib_nacional():
    assert fmt.cod_trib_nacional("010501") == "01.05.01"


def test_limit():
    assert fmt.limit("abcdef", 3) == "abc..."
    assert fmt.limit("ab", 3) == "ab"
