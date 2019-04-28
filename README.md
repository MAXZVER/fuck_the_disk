# fuck_the_disk

## Windows 
* pip install certifi
* pip install webdavclient

## For webdavclient need hack client.py lib for sertificates error

* Add in top of file client.py import certifi
* And add request.setopt(pycurl.CAINFO, certifi.where()) for all requests with error.
