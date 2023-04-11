### Face AI

Back in the innocent days when Dream had not done his face reveal, I was ready to cash in on some quick internet fame by finding his face using AI. So I leached off of some researchers by downloading their good code from github and wrote some generally bad code that would compare faces using the AI from the site in order to select the one most likely to be Dream from the dataset.

This was one of the more complicated scripts I made from that long ago, but if you're curious, it didn't work at all. It selected Dream as a woman nearly every time. I got tired of beating my head against the wall in Visual Studio on a bad laptop with code that took 15 minutes to run only to label dream a woman, so I gave up at some point.

The contents of the code in facevoice-master are not my own; the original readme has been included to indicate this. They are the product of research which can be found at http://facevoice.csail.mit.edu/. A copy of the code has been included with a few modifications to allow usage with modern tensorflow. The modification and distribution of the code is permitted under the MIT license under which it was originally published.

To run this code, you must place a pre-trained model in the facevoice-master directory. This model can be found on the website above (make sure to use voice as the reference modality). Unzip it in the directory, and the code should run decently well.

There is a specific format that the voice must be in that is specified by the researchers' repo. 

A face dataset is included in ./Faces but you can always add more or create a new dataset. I have no idea how I found this dataset, but it's there.

The Restructure_Images.py file? Yeah I have no idea what that does. It contains some nasty absolute paths, but I didn't adjust them because the things they point to don't even point to anything anymore. No idea what it's there fore.