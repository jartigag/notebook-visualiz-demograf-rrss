echo "Red social,Visitantes (EEUU),Visitantes (Mundo),Visitas (EEUU),Visitas (Mundo),Nivel Educ. Bajo,Nivel Educ. Medio,Nivel. Educ Alto,Sin hijos"
awk -OFS"," -F"," '{for (f=1;f<=NF;f++) col[f] = col[f]","$f} END {for (f=1;f<=NF;f++) print col[f]}' data.csv | cut -c2- | sort -t"," -nrk$1,$1
