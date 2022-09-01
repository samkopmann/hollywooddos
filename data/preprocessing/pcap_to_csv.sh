echo "Start $1"
tshark -r $1 -T fields -E header=y -E separator=, -E quote=d -E occurrence=f -e frame.time_relative -e ip.src -e ip.dst > $2
echo "Done"