# Add repo for cvmfs if needed:

        yum-config-manager --add-repo http://linuxsoft.cern.ch//cern/centos/7/cern/x86_64
        yum-config-manager --add-repo http://linuxsoft.cern.ch//cern/centos/7/cernonly/x86_64
        yum clean all
        yum install cvmfs cvmfs-config-default

# Install packges:
    CMake:
        * Install cmake: 
            yum install cmake3
            yum install cmake

    zlib-devel:
        * Install: yum install zlib-devel

    libx11-dev:
        * Install x11 lib: yum install libx11-dev

    Python:
        * Install Python3: yum install -y python36.x86_64 python36-libs.x86_64 python36-devel.x86_64 python36-pip
        * Set Python3 as default: ln -fs /usr/bin/python3 /usr/bin/python
        * Install python-tools: yum install python-tools

    ROOT:
    - Precompiled
        * Download latest version of ROOT: curl https://root.cern/download/root_v6.18.00.Linux-centos7-x86_64-gcc4.8.tar.gz --output root_v6.18.00.Linux-centos7-x86_64-gcc4.8.tar.gz
        * Unzip the archive: tar -xvf root_v6.18.00.Linux-centos7-x86_64-gcc4.8.tar.gz
        * Set-up ROOT: source root/bin/thisroot.sh

    - Sources
        * Download ROOT source code: curl https://root.cern/download/root_v6.18.00.source.tar.gz --output root_v6.18.00.source.tar.gz
        * Unzip the archive: tar -xvf root_v6.18.00.source.tar.gz
        * cd to root unzip and create build dir: mkdir builddir; cd builddir
        * Prepare for build: cmake3 -Dx11=OFF -Dxft=OFF ..
        * Build: cmake3 --build . --target install
        * Install: sudo cmake3 -DCMAKE_INSTALL_PREFIX=/home/root -DPYTHON_EXECUTABLE=/usr/bin/python3.6 -P cmake_install.cmake

# Clone the cmssw repo:
        git clone git@github.com:CMSTrackerDPG/cmssw.git

# Copy scripts from the old VM to the new one:
        mkdir -p /home/scripts
        cp -R /afs/cern.ch/user/c/cctrack/scratch0/* /home/scripts

# Set up CMSSW environment:
        * Move to the proper folder: cd /home/scripts/TKMap/CMSSW_X_X_X/src/
        * Set-up cms environment: cmsenv
        * Set-up ROOT: source root/bin/thisroot.sh

# Generate proxy for cmsRun
        * voms-proxy-init --cert /data/users/cctrkdata/current/auth/proxy/usercert.pem -k /data/users/cctrkdata/current/auth/proxy/userkey.pem

# Compiling CMSSW:
        * source /cvmfs/cms.cern.ch/cmsset_default.sh
        * cmsrel CMSSW_X_Y_Z (like cmsrel CMSSW_10_6_0)
        * cd CMSSW_X_Y_Z/src
        * cmsenv
        * git cms-init
        * git cms-addpkg DQM/SiStripMonitorClient
        * scram b (compile command)

# CMSSW - testing pull request
        * source /cvmfs/cms.cern.ch/cmsset_default.sh
         cmsrel CMSSW_X_Y_Z (like cmsrel CMSSW_10_6_0)
        * cd CMSSW_X_Y_Z/src
        * cmsenv
        * git cms-init
        * git fetch official-cmssw
        * git fetch official-cmssw pull/[pull request number]/head:[custom branch name]
        * git checkout [custom branch name]
        * git cms-addpkg DQM/SiStripMonitorClient
        * scram b (compile command)

# Add eos support:
        * https://cern.service-now.com/service-portal/article.do?n=KB0003846
        * yum install locmap(needs sudo)
        * locmap --enable eosclient; locmap --configure eosclient(both commands need sudo)

