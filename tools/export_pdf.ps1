# Export Mathew_Garcia_Resume.docx to Mathew_Garcia_Resume.pdf through Microsoft Word (Windows only).
#
#     powershell -ExecutionPolicy Bypass -File tools/export_pdf.ps1
#
# Run it after tools/build_docx.py so the PDF on the site matches the Word file. Word runs hidden with
# alerts off and is quit afterwards; the export takes about fifteen seconds. The PDF keeps the
# hyperlinks, carries the document title and author, and is tagged for screen readers.
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
# The [string] casts matter: Join-Path returns a PowerShell-wrapped string, and handing that wrapper
# to Word's ExportAsFixedFormat makes the hidden Word wait forever instead of writing the file.
$docx = [string](Join-Path $repo 'Mathew_Garcia_Resume.docx')
$pdf  = [string](Join-Path $repo 'Mathew_Garcia_Resume.pdf')

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0                                    # wdAlertsNone
try {
    $doc = $word.Documents.Open($docx, $false, $true)      # ConfirmConversions=false, ReadOnly=true
    # ExportAsFixedFormat(OutputFileName, ExportFormat=17 PDF, OpenAfterExport, OptimizeFor=0 print,
    #   Range=0 whole document, From, To, Item=0 content, IncludeDocProps, KeepIRM, CreateBookmarks=0,
    #   DocStructureTags, BitmapMissingFonts, UseISO19005_1)
    $doc.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 1, 1, 0, $true, $true, 0, $true, $true, $false)
    $doc.Close(0)                                          # wdDoNotSaveChanges
} finally {
    $word.Quit()
}
Write-Output ("wrote {0} ({1} bytes); open it to confirm it is still three pages" -f $pdf, (Get-Item $pdf).Length)
