# Work with CMSSW up to release 11_0_1
# Might work with further releases up to when the TkMap_script_phase1.py is replaced
# with TkMaps_from_eos.py

# Has to be added to the VMCMS066 home of the cctrack user

#!/usr/bin/env python3

import argparse
import subprocess
import os
import re

CMSSW_RELEASE = "CMSSW_11_0_1"
PATH = "/home/cctrack/" + CMSSW_RELEASE  + "/src/DQM/SiStripMonitorClient/scripts"
CERT = "/data/proxy/"
PROXY = "/tmp/x509up_trackermaps_proxy"

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Tracker Maps Script')
    parser.add_argument('run_type',
                       help='run type')
    parser.add_argument('min', type=int,
                       help='minimum run number')
    parser.add_argument('max', type=int,
                       help='maximum run number')

    args = parser.parse_args()

    return args

def check_CMSSW():
    if os.path.isdir("/home/cctrack/" + CMSSW_RELEASE):
        return

    list_of_commands = [
                        "/cvmfs/cms.cern.ch/cmsset_default.sh",
                        "cmsrel " + CMSSW_RELEASE,
                        "cd /home/cctrack/" + CMSSW_RELEASE  + "/src",
                        "cmsenv",
                        "git cms-init",
                        "git cms-addpkg DQM/SiStripMonitorClient",
                        "scram b",
                       ]

    process = subprocess.Popen(['/bin/csh', '-c'," && ".join(list_of_commands)], stdout=subprocess.PIPE).stdout
    print(process.read().decode())

def main():
    args = parse_arguments()

    # Ensure the user cannot use symbols that can be interpreted by csh
    pattern = re.compile("[a-zA-Z]+$")
    if not pattern.match(str(args.run_type)):
        print(str(args.run_type) + ": Wrong Run Type")
        return

    check_CMSSW()

    tracker_maps_command = "python " + PATH  + "/TkMap_script_phase1.py " + str(args.run_type) + " " + str(args.min) + " " + str(args.max)

    list_of_commands = [
                        "voms-proxy-init --cert " + CERT + "usercert.pem" + " -k " + CERT + "userkey.pem" + " -out " + PROXY,
                        "cp " + PROXY + " /eos/project-t/tkdqmdoc/private/proxy.cert",

                        "cd /home/cctrack/" + CMSSW_RELEASE  + "/src",
                        "cmsenv",
                        tracker_maps_command,
                       ]

    process = subprocess.Popen(['/bin/csh', '-c'," && ".join(list_of_commands)], stdout=subprocess.PIPE).stdout
    print(process.read().decode())

main()
