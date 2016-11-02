# dcos-in-a-box
The DC/OS-IN-A-BOX resource repository

## Prerequisites

- Intel NUC computers
- Network switch
- Network patch cables for each Intel NUC computer
- A bootstrap node with a working linux distribution and Python 3 and Docker.

## Prepare

1. Download a CentOS minimum distribution ISO. (TODO Add link)
2. Enter BIOS and adjust configuration:
   - Set time
   - Set fan profile to "Cool"
   - (Optional) Save profile as "DC/OS"
3. Install CentOS on each node
   - Language: English (US)
   - Keyboard: English (US)
   - Partitioning:
     - EFI system partition (200 MiB)
     - boot partition (500 MiB, ext4, no LVM, mount point `/boot`)
     - root partition (rest of space available, ext4, no LVM, mount point `/`)
   - Security policy: General purpose
   - Create **no additional users**.
   - Choose a root password that has to be the same on all machines.
4. Configure CentOS:
   1. Connect to internet.
   2. Update packages:

      ```sh
      yum update
      ```

   3. Be sure that all machines accept and handle incoming ICMP requests / pings.
      You can check that by executing

      ```sh
      cat /proc/sys/net/ipv4/icmp_echo_ignore_all
      ```

      `0` means that ICMP is enabled, `1` means disabled.

   4. Configure static IP addresses on each machine:
     - Bootstrap node: `1.0.0.0`
     - Master nodes: `1.0.10.0-255`
     - Private agent nodes: `1.0.20.0-255`
     - Public agent nodes: `1.0.30.0-255`

# Setup

1. **Turn on all master and agent nodes.**
2. Run `install.py`
