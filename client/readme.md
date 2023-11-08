1. Client side of Omniclient designed to run on:
    1.1. Container: Docker, LXC that use Linux
    1.2. VM: Linux-installed VM that can connected to Admin section through LAN
2. System requirements
    2.1. Operative System
        2.1.1. Linux or Linux-based OS 
    2.2. Python
        2.2.1. Version: 3.10+
        2.2.2. Snakemake workflow designer
        2.2.3. On Docker containers
            2.2.3.1. Python scripts MUST INSIDE CONTAINER
            2.2.3.2. Snakemake can output results to output folder its job level
        2.2.4. On VM and LXC containers
            2.2.3.1. It is recommended to installed it alongside with bash scripts
            2.2.3.2. In case the install location must be done in separated area, make sure to edit the location on bash scripts
    2.3. Linux shell
        2.3.1. With Docker containers
            2.3.1.1. Containers must be hosted and stored inside VM or Container that host Admin section of Omniclient
            2.3.1.2. Bash script can be stored outside and command will be executed inside the docker container
            2.3.1.3. Extra scripts most be used to extract output, contacts software designer for extra script
        2.3.2. On VM and LXC containers
            2.3.2.1. Make sure the OS is up-to-date or in stable version
            2.3.2.2. In case required for update OS, please backup the configurations first
