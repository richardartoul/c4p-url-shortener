# URL Shortener

## Overview

This repository contains a proof of concept URL shortener for demonstration and educational purposes.

URL short code can be created by posting to the root "/" of the web server with an appropriate JSON payload. Example:

```
POST http://localhost:5000/
```

```json
{
  "url": "https://wwww.google.com",
  "short_code: "google"
}
```

Once a short code has been created, it can be used by issuing a GET request to the root "/" of the web server with the short code provided as a query argument. Example:

```
http://localhost:5000?short_code=google
```