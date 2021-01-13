
# POST /compare/images
This API just has one endpoint: `/compare/images`
It will only accept POST requests.

You must pass an API key with each request.  The API Key can be any non-empty string.

A successful response should have the following format:
```
{"data": {"similarity": "100.0%"}}
```

## Sending Images
There are two ways to upload images to this endpoint.  

You can upload files from your local system, or you can upload images that come from remote servers via their URLs.

If you want to upload an image from a URL, POST a JSON payload with the following key/value pairs: 
{
    "image1_location": "<url_of_image1>",
    "image2_location": "<url_of_image2>"
}


## Sample cURL Requests to Test With

### Compare local files
```
curl -i -F 'image1=@/<file/path/to/an/image.jpg>' -F 'image2=@/<file/path/to/an/image.jpg>' <hostname>:5000/compare/images -H "x-api-key:qwertyuiop"
```

### Compare files from URLs
```
curl -i -X POST -H "x-api-key:qwertyuiop" -H "Content-Type: application/json" -d '{"image1_location": "<https://remote-server.com/image1.jpg>", "image2_location": "<https://remote-server.com/image1.jpg>' <hostname>:5000/compare/images
```