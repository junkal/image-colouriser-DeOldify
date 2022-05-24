# image_colouriser_DeOldify

This repository implements the DeOldify pre-trained image colourisation model into a Flask API. The pre-trained image colourisation model is provided thanks to the great work by the [DeOldify Team](https://deoldify.ai/). The instruction to get the pre-trained model can be found in their [Github](https://github.com/jantic/DeOldify). There are 2 pre-trained models - Artistic and Stable. Information about these 2 models can be found in the readme file of the DeOldify Github. 

This repository wraps the **Stable** model into the Flask API. The repo is grouped into 2 folders - Server and App. The names should be quite self-explanatory. The _server.py_ file in the Server directory runs the Flask server, look for the Stable pretrained model with file name _ColorizeStable_gen.pth_ in the models directory. If the found is not found, then it will download a copy of the model weight from the DeOldify shared directory. The App folder implements the _process_ command which issues a POST request to the server. All return colourised images are saved in the _post_responses_ folder.

Terminal 1 (server):
> cd server
> python server.py

Terminal 2 (app):
> cd app
> python post_image.py --image path/to/image/with/extension

The pre-trained model provides pretty good quality image colourisation. Some samples provided below. The left images are the original images while and right images are the colourised images.

![image](https://user-images.githubusercontent.com/6497242/170080012-c1bca7c6-531b-4606-8bc2-f2aa85c017c8.png)

![image](https://user-images.githubusercontent.com/6497242/170080168-a950458e-3518-4ac9-83f5-2cbb3b319c76.png)

![image](https://user-images.githubusercontent.com/6497242/170080259-3966a25b-0694-42a8-a8b4-29bfae370212.png)
