import subprocess
import os,sys

domain =sys.argv[1]
print domain

#os.chdir("/opt")

#subprocess.call("cd /opt",shell=True)
#subprocess.call("ls")

subprocess.call(["scrapy","crawl","yunxi","-a","search_host={}".format(domain)],cwd="/data/yunxi")
#subprocess.call("whatweb", "-v" ,"-a", "3", "{}".format(domain))
