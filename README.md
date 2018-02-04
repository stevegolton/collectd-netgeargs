# collectd-netgeargs
A collectd exec "plugin" for scraping netger gs10X series switch webpages for port usage status. All values are in bits.

## Requirements
```
pip3 install -r requirements.txt
```

## Usage

To run manually:

```
python3 gs.py <switch_hostname> <password>
```

Or in collectd.conf
```
LoadPlugin exec

<Plugin exec>
        Exec "user:group" "python3" "/path/to/gs.py" "myswitch.local" "supers3cretpassword"
</Plugin>
```

Note: Don't try to get collectd to run it as root, it won't let you. I'm not sure if there's a way to force it but it's not a good idea anyway.

I realise the exec plugin is not a good way to get collectd to run python script, there is a perfectly good python plugin for that - but this way it keeps things simple and means the python script can be run from the command line as well.

Remember to add rxPkt, txpkt (yes, that's a lower case 'p' in txpkt) and crcPkt to your types.db file.

```
rxPkt                   value:GAUGE:0:U
txpkt                   value:GAUGE:0:U
crcPkt                  value:GAUGE:0:U
```

or if you want collectd to find the derivitive data rates:

```
rxPkt                   value:DERIVE:0:U
txpkt                   value:DERIVE:0:U
crcPkt                  value:DERIVE:0:U
```
