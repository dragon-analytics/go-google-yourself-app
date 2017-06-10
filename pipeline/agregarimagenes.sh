docker service create --name dpa-registry --publish 5000:5000 registry:2

docker tag dpa/luigi-worker localhost:5000/dpa/luigi-worker:0.2

docker push localhost:5000/dpa/luigi-worker:0.2

docker tag dpa/luigi-server localhost:5000/dpa/luigi-server:0.2

docker push localhost:5000/dpa/luigi-server:0.2

docker tag dpaequipo10/test-python-lda localhost:5000/dpaequipo10/test-python-lda:latest

docker push localhost:5000/dpaequipo10/test-python-lda:latest

docker tag dpaequipo10/test-python-mail localhost:5000/dpaequipo10/test-python-mail:latest

docker push localhost:5000/dpaequipo10/test-python-mail:latest

docker tag dpaequipo10/test-python-ubicaciones localhost:5000/dpaequipo10/test-python-ubicaciones:latest

docker push localhost:5000/dpaequipo10/test-python-ubicaciones:latest

docker tag dpaequipo10/test-python-freqmail localhost:5000/dpaequipo10/test-python-freqmail:latest

docker push localhost:5000/dpaequipo10/test-python-freqmail:latest

docker tag dpaequipo10/test-python-freqbusq localhost:5000/dpaequipo10/test-python-freqbusq:latest

docker push localhost:5000/dpaequipo10/test-python-freqbusq:latest

docker tag dpaequipo10/test-python-ubicacioneshtml localhost:5000/dpaequipo10/test-python-ubicacioneshtml:latest

docker push localhost:5000/dpaequipo10/test-python-ubicacioneshtml:latest

