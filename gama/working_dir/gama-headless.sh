#!/bin/bash

# Establecer la memoria para GAMA
memory=2048m

# Inicializar variables
declare -i i
i=0

# Registrar el inicio del script
echo "Starting gama-headless.sh script" >> /working_dir/gama-headless.log
echo ${!i} >> /working_dir/gama-headless.log

# Procesar los argumentos
for ((i=1;i<=$#;i=$i+1))
do
if test ${!i} = "-m"
then
    i=$i+1
    memory=${!i}
else
    PARAM=$PARAM\ ${!i}
    i=$i+1
    PARAM=$PARAM\ ${!i}
fi
done

# Registrar la versión de GAMA
echo "******************************************************************" >> /working_dir/gama-headless.log
echo "* GAMA version 1.9.3                                             *" >> /working_dir/gama-headless.log
echo "* http://gama-platform.org                                       *" >> /working_dir/gama-headless.log
echo "* (c) 2007-2023 UMI 209 UMMISCO IRD/UPMC & Partners              *" >> /working_dir/gama-headless.log
echo "******************************************************************" >> /working_dir/gama-headless.log

# Crear un directorio de trabajo temporal
passWork=.work$RANDOM

# Establecer el classpath de GAMA
GAMA_CLASSPATH=$(find /opt/gama -name "*.jar" | tr '\n' ':')

# Asegurarse de que Java esté en el PATH
export PATH="/usr/lib/jvm/java-17-openjdk-amd64/bin:${PATH}"

# Ejecutar GAMA en modo headless
echo "Running GAMA with parameters: $PARAM" >> /working_dir/gama-headless.log
java -cp $GAMA_CLASSPATH -Xms512m -Xmx$memory -Djava.awt.headless=true org.eclipse.core.launcher.Main -application msi.gama.headless.id4 -data $passWork $PARAM >> /working_dir/gama-headless.log 2>&1

# Registrar el final de la ejecución de GAMA
echo "GAMA execution finished" >> /working_dir/gama-headless.log

# Eliminar el directorio de trabajo temporal
# rm -rf $passWork