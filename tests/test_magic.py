# encoding: utf-8


import magic

mpath = 'config/magic/magic.mgc'
m = magic.Magic(magic_file=mpath)


def test_pdf13():
    path = 'tests/testdata/test-indesign-pdf-1.3.pdf'
    result = m.from_file(path, mime=True)
    assert result == 'application/pdf'


def test_pdf14():
    path = 'tests/testdata/test-indesign-pdf-1.4.pdf'
    result = magic.from_file(path, mime=True)
    assert result == 'application/pdf'


def test_pdf15():
    path = 'tests/testdata/test-indesign-pdf-1.5.pdf'
    result = magic.from_file(path, mime=True)
    assert result == 'application/pdf'


def test_pdf16():
    path = 'tests/testdata/test-indesign-pdf-1.6.pdf'
    result = magic.from_file(path, mime=True)
    assert result == 'application/pdf'


def test_pdf17():
    path = 'tests/testdata/test-indesign-pdf-1.7.pdf'
    result = magic.from_file(path, mime=True)
    assert result == 'application/pdf'


def test_libreoffice_odf_table_ods():
    path = 'tests/testdata/test-libreoffice-odf-table.ods'
    result1 = magic.from_file(path)
    assert result1 == 'OpenDocument Spreadsheet'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.oasis.opendocument.spreadsheet'


def test_libreoffice_odt():
    path = 'tests/testdata/test-libreoffice-odt.odt'
    result1 = magic.from_file(path)
    assert result1 == 'OpenDocument Text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.oasis.opendocument.text'


def test_libreoffice_open_xml_table():
    path = 'tests/testdata/test-libreoffice-office-open-xml-table.xlsx'
    result1 = magic.from_file(path)
    assert result1 == 'OpenDocument Text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def test_libreoffice_office_open_xml_text():
    path = 'tests/testdata/test-libreoffice-office-open-xml-text.docx'
    result1 = magic.from_file(path)
    assert result1 == 'OpenDocument Text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.oasis.opendocument.text'


def test_libreoffice_open_document_flat_xml_fodt():
    path = 'tests/testdata/test-libreoffice-open-document-flat-xml.fodt'
    result1 = magic.from_file(path)
    assert result1 == 'XML document text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/xml'


def test_libreoffice_open_document_spreadsheet_fods():
    path = 'tests/testdata/test-libreoffice-open-document-spreadsheet.fods'
    result1 = magic.from_file(path)
    assert result1 == 'XML document text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/xml'


def test_libreoffice_openoffice_table_sxc():
    path = 'tests/testdata/test-libreoffice-openoffice-table.sxc'
    result1 = magic.from_file(path)
    assert result1 == 'OpenOffice.org 1.x Calc spreadsheet'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.sun.xml.calc'


def test_libreoffice_openoffice_sxw():
    path = 'tests/testdata/test-libreoffice-openoffice-sxw.sxw'
    result1 = magic.from_file(path)
    assert result1 == 'OpenOffice.org 1.x Writer document'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.sun.xml.writer'


def test_libreoffice_unified_office_spreadsheet_uos():
    path = 'tests/testdata/test-libreoffice-unified-office-format-spreadsheet.uos'
    result1 = magic.from_file(path)
    assert result1 == 'XML document text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/xml'


def test_libreoffice_unified_office_uot():
    path = 'tests/testdata/test-libreoffice-unified-office-format.uot'
    result1 = magic.from_file(path)
    assert result1 == 'XML document text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/xml'


def test_word_97_2004_doc():
    path = 'tests/testdata/test-word-97-2004.doc'
    result1 = magic.from_file(path)
    assert 'Word' in result1
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/msword'


def test_word_docx():
    path = 'tests/testdata/test-word-docx.docx'
    result1 = magic.from_file(path)
    assert result1 == 'Microsoft Word 2007+'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'


def test_word_2003_xml():
    path = 'tests/testdata/test-word-2003-xml.xml'
    result1 = magic.from_file(path)
    assert result1 == 'XML document text'
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/xml'


def test_word_rtf():
    path = 'tests/testdata/test-word-rtf.rtf'
    result1 = magic.from_file(path)
    assert 'Rich Text Format' in result1
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'text/rtf'


def test_excel_xls():
    path = 'tests/testdata/test-excel-xls.xls'
    result1 = magic.from_file(path)
    assert 'Excel' in result1
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.ms-excel'


def test_excel_xlsx():
    path = 'tests/testdata/test-excel-xlsx.xlsx'
    result1 = magic.from_file(path)
    assert 'Microsoft Excel 2007+' in result1
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def test_powerpoint_pptx():
    path = 'tests/testdata/test-powerpoint-pptx.pptx'
    result1 = magic.from_file(path)
    assert 'Microsoft PowerPoint 2007+' in result1
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.openxmlformats-officedocument.presentationml.presentation'


def test_powerpoint_ppt():
    path = 'tests/testdata/test-powerpoint-ppt.ppt'
    result1 = magic.from_file(path)
    assert 'PowerPoint' in result1
    result2 = magic.from_file(path, mime=True)
    assert result2 == 'application/vnd.ms-powerpoint'


def test_various_word_formats():
    """
    The point here is that the various formats use different mime types.
    """
    path1 = 'tests/testdata/test-word-docx.docx'
    path2 = 'tests/testdata/test-word-97-2004.doc'
    assert magic.from_file(path1, mime=True) != magic.from_file(path2, mime=True)
