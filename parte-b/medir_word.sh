#!/usr/bin/env bash
# Abre el Word en Word de Windows, actualiza el índice, cuenta las páginas y exporta el PDF.
set -e
T=/mnt/c/Users/justo/AppData/Local/Temp/tp3b
mkdir -p "$T"
cp "$(dirname "$0")/26C2-G05-SIM-RedBaires.docx" "$T/informe.docx"
powershell.exe -NoProfile -Command "
\$w = New-Object -ComObject Word.Application; \$w.Visible = \$false
\$d = \$w.Documents.Open('C:\Users\justo\AppData\Local\Temp\tp3b\informe.docx')
foreach (\$t in \$d.TablesOfContents) { \$t.Update() }
\$d.Repaginate()
'paginas: ' + \$d.ComputeStatistics(2)
\$d.Save()
\$d.SaveAs2('C:\Users\justo\AppData\Local\Temp\tp3b\informe.pdf', 17)
\$d.Close(0); \$w.Quit()" | tr -d '\r'
cp "$T/informe.docx" "$(dirname "$0")/26C2-G05-SIM-RedBaires.docx"
cp "$T/informe.pdf" "$(dirname "$0")/26C2-G05-SIM-RedBaires.pdf"
