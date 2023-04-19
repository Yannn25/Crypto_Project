if [ ! -d class ]; then 
    mkdir class
fi

javac -d class Main.java

java -Xmx4096m -cp class Main $1 $2 $3 