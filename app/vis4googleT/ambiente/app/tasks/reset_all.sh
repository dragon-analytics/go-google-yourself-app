echo 1 > /tmp/todas_busquedas.json
echo 1 > /tmp/todas_ubicaciones.json
echo 1 > /tmp/todo_googlet.zip
echo 1 > /tmp/todos_mails.mbox
mkdir /tmp/Takeout

R CMD BATCH tasks/init_inds.R
python tasks/ups/reset_indicadores.py
./tasks/clear_tmp.sh
 rm *.Rout

