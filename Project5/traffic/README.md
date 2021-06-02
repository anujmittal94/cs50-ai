# Observations during testing

## load_data

The gtsrb database contained category folders containing images which needed to
loaded in as numpy arrays.

- To access directories the scandir function from the os directory was used
- Besides being faster than prior listdir usage, scandir had the additional advantage
  of automatically dealing with path component separators and being platform independent
- imread from OpenCV-Python converts the image into an array, which is resized using
  the resize function

## get_model
- Adapting the convolutional model from the lecture directly resulted in a low accuracy
- Adding more convolutional layers significantly increased the accuracy
- Max pooling was used after each convolutional layer, this significantly improved training
  speed while increasing accuracy and decreasing loss
- More filters were used deeper in the network as we got closer to the output shape
- As we were working with images, a convolutional model proved to be most effective
- Depending on number of nodes and layers, dropout had a different threshold for positive or
  negative impact on the loss and accuracy
- A functional model may prove to be more effective rather than a sequential one
- While the model was accurate predicting images from the dataset, it wasn't very
  effective with random images of traffic signs from external sources
