# Python Internet Archive Downloader
## Short Version
Restore **all ressources** from a given domain from the wayback machine for a given time period, **group these resources by mimetype** and save it to local disk. Functional approach in less than 100 lines of code.

## Long Version
As a side project i tried to restore a old webpage. I found out, that these page is backuped in the waxbackmachine. The tools i found to download all ressource of these page from the way back CDX Server are chargeable or group the ressources by url path. That was not i want because i have to deal with complex folderstructures.

# Flow Chart
- mermaid
- generate meta data in a seperate json file called x. this file wil map the file name to the original url.

# Usage
The functionality of these repository **based on the python standard library**. So there is no need for a requirements.txt file ct.
```
python main.py --domain xxl-angeln.de --start 20070101000000 --end 20131231000000

Required Arguments:
    --domain            The domain you want to download
    --start             Startdate in yyyyMMddhhmmss
    --end               Enddate in yyyyMMddhhmmss
```
If there are any erros during runntime these errors are logged in ```log.log``` in the root folder.

# Contribution
Feel free.