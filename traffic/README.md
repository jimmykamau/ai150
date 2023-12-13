# Experimentation Process for Neural Network Trained on GTSRB

## Initial Model

The initial model (similar to the one used in the handwriting lecture) consists of the following layers:
- A 2D convolution layer with 32 filters
- A max-pooling layer of size 2*2
- A flattening layer
- A dense hidden layer of 128 units
- A dropout layer with a rate of 50%
- A dense output layer of NUM_CATEGORIES units

I used the modified dataset with 3 types of signs to test the code. It achieved a loss of `1.7739e-09` and accuracy of `1.0`, which indicated overfitting due to the small sample size.
I retrained the model with the full 43-category dataset, obtaining a loss of `3.5069` and accuracy of `0.0556`.

## Experimentation Log

#### Experiment 1: Testing on Subset
- **Changes:** Set `NUM_CATEGORIES` to 10 to test on a subset of data.
- **Results:** `loss: 2.1870 - accuracy: 0.1515 - 918ms/epoch - 7ms/step` Marked speed improvement, but accuracy is still low. A good starting point for further experimentation.

#### Experiment 2: Adding Convolutional and Pooling Layers
- **Changes:** Added one extra convolutional and pooling layer.
- **Results:** `loss: 0.2205 - accuracy: 0.9336 - 932ms/epoch - 8ms/step` Significant jump in accuracy observed.

#### Experiment 3: Adjusting Filters in Convolutional Layers
- **Changes:** Increased and decreased the number of filters in convolutional layers.
- **Results:** Accuracy dropped with a higher number of filters.

#### Experiment 4: Modifying Pool Size
- **Changes:** Adjusted pool size in pooling layers.
- **Results:** Changing pool size did not show a consistent improvement. The impact on training speed varied.

#### Experiment 5: Dropout Variation
- **Changes:** Adjusted dropout rate in the hidden dense layer to `0.3`. Also increased convolution layers filters to `256` and pool size to `(4, 4)`.
- **Results:** `loss: 0.1360 - accuracy: 0.9629 - 2s/epoch - 16ms/step` Lower dropout improved accuracy, indicating that regularization might have been too aggressive.

#### Experiment 6: Increasing Output Categories
- **Changes:** Increased `NUM_CATEGORIES` to 20 and 30.
- **Results:** `loss: 0.2068 - accuracy: 0.9468 - 3s/epoch - 11ms/step` Accuracy slightly reduced with a higher number of categories while increased training time.

#### Experiment 7: Reducing Pool Size
- **Changes:** Reduced pool size to `(2, 2)` in pooling layers.
- **Results:** `loss: 0.1705 - accuracy: 0.9588 - 4s/epoch - 15ms/step` Training speed increased, but accuracy remained consistent.

#### Experiment 8: Further Dropout Adjustment
- **Changes:** Reduced dropout to `0.1`.
- **Results:** `loss: 0.1622 - accuracy: 0.9650 - 4s/epoch - 14ms/step` Accuracy slightly improved.

#### Experiment 9: Training on Full Dataset
- **Changes:** Tested on the full dataset.
- **Results:** `loss: 0.2720 - accuracy: 0.9461 - 5s/epoch - 15ms/step` Training is slow, and accuracy is reasonable but not optimal.

#### Experiment 10: Fine-tuning Filters and Dropout
- **Changes:** Adjusted convolution layer filters to `64`, used `128` units in the dense layer and increased dropout to `0.3`.
- **Results:** `loss: 0.1636 - accuracy: 0.9609 - 6s/epoch - 17ms/step` Improved accuracy.

## Conclusion

At this point, I was satisfied with the accuracy of the model. Further steps can be taken to fine-tune it and reduce its training time.