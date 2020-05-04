bash clean.sh
latexmk -pdf -shell-escape $1".tex"
open $1".pdf"
bash clean.sh
