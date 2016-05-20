import os
from tornado.options import define
from pprint import pprint

# noinspection PyPackageRequirements
class Config(object):
    def __init__(self):
        self.environment = 'dev'

        # TEMP to globally store timestamp of last "addConsumption" call, to assign the same timestamp to all consumptions in one round.
        #self.addConsumptionTimestampStore = 0

    def SetEnvVars(self, environment):

        self.logLocation = '/var/log/movie/'
        self.socketServerPort = 9999
        self.debug = False
        self.moviePORT = '80'

        if self.environment == 'dev':
            self.movieURL = 'http://10.211.55.100'
            self.debug = True

        self.clusterNodes = ['10.211.55.101', '10.211.55.102', '10.211.55.103']
        self.clusterName = "DSC Cluster"

        define("cluster_nodes", default=self.clusterNodes, help="cluster nodes")
        define("cluster_name", default=self.clusterName, help="cluster name")
        define("debug", default=self.debug, type=bool)






