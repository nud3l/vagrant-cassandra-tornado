# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant Cassandra Project
# https://github.com/bcantoni/vagrant-cassandra
# Brian Cantoni

# This template sets up 4 VMs:
#   node0: OpsCenter installed
#   node1-3: only Java installed
# See the README for a walkthrough explaining the installation process through OpsCenter.

# Adjustable settings
CFG_MEMSIZE = "3000"    # max memory for each VM
CFG_TZ = "Europe/Berlin"   # timezone, like US/Pacific, US/Eastern, UTC, Europe/Warsaw, etc.
SERVER_COUNT = 4
NETWORK = '10.211.55.'
FIRST_IP = 100

# if local Debian proxy configured (DEB_CACHE_HOST), install and configure the proxy client
deb_cache_cmds = ""
if ENV['DEB_CACHE_HOST']
  deb_cache_host = ENV['DEB_CACHE_HOST']
  deb_cache_cmds = <<CACHE
apt-get install squid-deb-proxy-client -y
echo 'Acquire::http::Proxy "#{deb_cache_host}";' | sudo tee /etc/apt/apt.conf.d/30autoproxy
echo "Acquire::http::Proxy { debian.datastax.com DIRECT; };" | sudo tee -a /etc/apt/apt.conf.d/30autoproxy
cat /etc/apt/apt.conf.d/30autoproxy
CACHE
end

# Provisioning script for Opscenter node (node0)
opsc_script = <<SCRIPT
#!/bin/bash
cat > /etc/hosts <<EOF
127.0.0.1       localhost

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

10.211.55.100   node0
10.211.55.101   node1
10.211.55.102   node2
10.211.55.103   node3
EOF

# set timezone
echo "#{CFG_TZ}" > /etc/timezone    
dpkg-reconfigure -f noninteractive tzdata

#{deb_cache_cmds}

# add DataStax repo for APT
echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/datastax.community.list
wget -q -O - http://debian.datastax.com/debian/repo_key | sudo apt-key add -
apt-get update

# install OpsCenter and a few base packages
apt-get install vim curl zip unzip git python-pip opscenter -y

# start OpsCenter
service opscenterd start

# Setup tornado server
mkdir /var/www
chmod 777 /var/www
mkdir /var/log/movie
apt-get install python -y
apt-get install build-essential python-dev -y
apt-get install libev4 libev-dev -y

echo "Vagrant provisioning complete and OpsCenter started"
SCRIPT

# Provisioning script for Cassandra nodes (node1-3)
node_script = <<SCRIPT
#!/bin/bash
cat > /etc/hosts <<EOF
127.0.0.1       localhost

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

10.211.55.100   node0
10.211.55.101   node1
10.211.55.102   node2
10.211.55.103   node3
EOF

# set timezone
echo "#{CFG_TZ}" > /etc/timezone    
dpkg-reconfigure -f noninteractive tzdata

#{deb_cache_cmds}

# install Java and a few base packages
add-apt-repository ppa:openjdk-r/ppa
apt-get update
apt-get install vim curl zip unzip git python-pip openjdk-8-jdk -y

echo "Vagrant provisioning complete"
SCRIPT


# Configure VM servers
servers = []
(0..SERVER_COUNT-1).each do |i|
  name = 'node' + i.to_s
  ip = NETWORK + (FIRST_IP + i).to_s
  servers << {'name' => name, 'ip' => ip}
end

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  servers.each do |server|
    config.vm.define server['name'] do |config2|
      config2.vm.hostname = server['name']
      config2.vm.network :private_network, ip: server['ip']

      if (server['name'] == 'node0')
        config2.vm.provision :shell, :inline => opsc_script
      else
        config2.vm.provision :shell, :inline => node_script
      end

      config2.vm.provider "vmware_fusion" do |v|
        v.vmx["memsize"]  = CFG_MEMSIZE
      end
      config2.vm.provider :virtualbox do |v|
        v.name = server['name']
        v.customize ["modifyvm", :id, "--memory", CFG_MEMSIZE]
      end

    end
  end
end
