ip netns add red
ip netns add blue
ip netns add router 

ip link add eth0 type veth peer name eth1
ip link add eth2 type veth peer name eth3

ip link set eth0 netns red
ip link set eth1 netns router
ip link set eth2 netns router 
ip link set eth3 netns blue

ip netns exec red ip link set lo up
ip netns exec router ip link set lo up
ip netns exec blue ip link set lo up

ip netns exec red ip link set eth0 up
ip netns exec router ip link set eth1 up
ip netns exec router ip link set eth2 up
ip netns exec blue ip link set eth3 up

ip netns exec red ip address add 10.0.0.1/24 dev eth0
ip netns exec router ip address add 10.0.0.2/24 dev eth1
ip netns exec router ip address add 10.0.1.1/24 dev eth2
ip netns exec blue ip address add 10.0.1.2/24 dev eth3

ip netns exec red ip route add default via 10.0.0.2 dev eth0
ip netns exec blue ip route add default via 10.0.1.1 dev eth3

ip netns exec router sysctl -w net.ipv4.ip_forward=1