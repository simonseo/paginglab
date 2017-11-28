mkdir output
mkdir output-debugging
mkdir output-showrandom

cd output
for i in {10..16}
  do
    curl "https://cs.nyu.edu/~gottlieb/courses/os202/labs/lab4/run-$i" > run-$i.txt
  done
for i in {1..9}
  do
    curl "https://cs.nyu.edu/~gottlieb/courses/os202/labs/lab4/run-0$i" > run-0$i.txt
  done
cd ..

cd output-debugging
for i in {10..16}
  do
    curl "https://cs.nyu.edu/~gottlieb/courses/os202/labs/lab4/run-$i-debug" > run-$i-debug.txt
  done
for i in {1..9}
  do
    curl "https://cs.nyu.edu/~gottlieb/courses/os202/labs/lab4/run-0$i-debug" > run-0$i-debug.txt
  done
cd ..

cd output-showrandom
for i in {10..16}
  do
    curl "https://cs.nyu.edu/~gottlieb/courses/os202/labs/lab4/run-$i-show-random" > run-$i-show-random.txt
  done
for i in {1..9}
  do
    curl "https://cs.nyu.edu/~gottlieb/courses/os202/labs/lab4/run-0$i-show-random" > run-0$i-show-random.txt
  done
cd ..
