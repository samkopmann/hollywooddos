#!/bin/bash
mergecap ../datasets/ddos-2007/*.pcap -w ../datasets/ddos-2007/ddos.pcap
editcap ../datasets/ddos-2007/ddos.pcap -i 150 ../datasets/ddos-2007/ddos.pcap
rm ../datasets/ddos-2007/ddostrace*
rm ../datasets/ddos-2007/ddos.pcap

for i in {11..13}
do
    ./pcap_to_csv.sh ../datasets/ddos-2007/ddos_*00$i*_2007*.pcap ../datasets/ddos-2007/ddos-$i.csv
done

rm ./datasets/ddos-2007/*pcap