# Overview :
  - Build and execute Docker containers to set up Flask web-service.
  - The Service will receive the image (via POST) and perform the analysis of the image behavior (via Google's [im2txt][tensorflow/models] open source project).
  - Just three steps.

# Environment requirements :
  - Install [Docker][Docker-officeSite] on your PC(macOS, Windows, linux)

# Before clone this repostory :
  - A pre-trained model can be downloaded at [here][pre-trained].
  - Put the file in the "chkpt" folder.
  - The folder structure is as follows.
  - chkpt
  - ⊦ model.ckpt-1000000.data-00000-of-00001
  - ⊦ model.ckpt-1000000.meta
  - ⊦ model.ckpt-1000000.index  
  - ⨽ word_counts.txt

# Start doing :
  - Use the terminal to move to the root directory. (The following is an example of macOS instructions)
> STEP 1  (Build image by Dockerfile)
  - The command is : docker build -t image-name:tag .
  - Replace image-name with your name
  - Replace tag with your label
  - ex. 
```sh
$ docker build -t first-image:latest .
```

> STEP 2  (Run image)
  - List of images & Find your image id
```sh
$ docker images
```
  - Run by image id.
  - The command is : docker run -p 5000:5000 -i -t image-id
  - ex.
```sh
$ docker run -p 5000:5000 -i -t 938ddb14e4d8
```
  - And you can see return log :
```sh
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

> STEP 3  (Test by Curl)
  - Prepare a JPEG or PNG image.
  - The command is : curl -v -F image=@<image path> http://localhost:5000/inference
  - ex.
```sh
$ curl -v -F image=@folder/test.jpg http://localhost:5000/inference
```

> Result
   - JSON format
```
[
  {
    "caption": "a slice of pizza sitting on top of a white plate .", 
    "p": 0.0037768055172771216
  }, 
  {
    "caption": "a slice of pizza on a white plate .", 
    "p": 0.001855960700329915
  }, 
  {
    "caption": "a slice of pizza on a white plate", 
    "p": 0.0008495462407023139
  }
]
```

   [tensorflow/models]: <https://github.com/tensorflow/models>
   [Docker-officeSite]: <https://www.docker.com/>
   [pre-trained]: <https://ibm.ent.box.com/v/show-and-tell-pretrained>
