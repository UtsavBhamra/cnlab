from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopology(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        h1 = self.addHost('h1',ip='10.0.0.1/24')
        h2 = self.addHost('h2',ip='10.0.0.2/24')
        h3 = self.addHost('h3',ip='10.0.0.3/24')
        h4 = self.addHost('h4',ip='10.0.0.4/24')

        self.addLink(s1,s2,cls=TCLink,bw=10,delay='10ms')
        self.addLink(s1,s3,cls=TCLink,bw=10,delay='10ms')

        self.addLink(h1,s2,cls=TCLink,bw=10,delay='10ms')
        self.addLink(h2,s2,cls=TCLink,bw=10,delay='10ms')
        self.addLink(h3,s3,cls=TCLink,bw=10,dealy='10ms')
        self.addLink(h4,s3,cls=TCLink,bw=10,delay='10ms')

def run_custom_topology():
    topo = CustomTopology()
    net = Mininet(topo=topo,link=TCLink)
    net.start()

    dumpNodeConnections(net.hosts)

    net.interact()
    net.stop()

if __name__=="__main__":
    setLogLevel('info')
    run_custom_topology()