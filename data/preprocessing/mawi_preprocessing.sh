editcap ../datasets/mawi/mawi_201909011400.pcap -i 150 ../datasets/mawi/mawi_background.pcap
rm ../datasets/mawi/mawi_201909011400.pcap
for i in {0..5}
do
    ./pcap_to_csv.sh ../datasets/mawi/mawi_background_*00${i}_2019*.pcap ../datasets/mawi/mawi_background-$i.csv
done
rm ../datasets/mawi/*.pcap
rm ../datasets/mawi/mawi_background.csv
