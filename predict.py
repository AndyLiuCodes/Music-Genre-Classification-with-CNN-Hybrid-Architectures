from keras.models import Sequential, Model, load_model
from keras_preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np

model_file = './best_model.h5'
BATCH_SIZE_TEST = 1
IMAGE_SIZE = (128, 128)

def append_ext(fn):
    return fn+".jpg"

def predict():
    testdf = pd.read_csv('./Data/test.csv',
                     names=["ID", "Class"], dtype=str)
    
    testdf["ID"] = testdf["ID"].apply(append_ext)

    test_datagen = ImageDataGenerator(rescale=1./255.)

    test_generator = test_datagen.flow_from_dataframe(
        dataframe=testdf,
        directory="./Data/Test/",
        x_col="ID",
        y_col="Class",
        batch_size=BATCH_SIZE_TEST,
        shuffle=False,
        class_mode="categorical",
        target_size=IMAGE_SIZE)

    STEP_SIZE_TEST = test_generator.n // test_generator.batch_size
    
    model = load_model(model_file)

    scores = model.evaluate_generator(generator=test_generator, steps=STEP_SIZE_TEST, verbose=1, workers=0)
    #PREDICT AGAIN AFTER!!!
    print("Evaluated Model")
    print("{}: {}, {}: {}".format(model.metrics_names[0], scores[0], model.metrics_names[1], scores[1]))
    
    test_generator.reset()
    print("Predicted Values")

    pred = model.predict_generator(test_generator,
                                steps=STEP_SIZE_TEST,
                                verbose=1)
    predicted_class_indices = np.argmax(pred, axis=1)

    # Fetch labels from train_gen & set predictions into 1D array
    labels = (test_generator.class_indices)
    labels = dict((v, k) for k, v in labels.items())
    predictions = [labels[k] for k in predicted_class_indices]

    # Calculate test accuracy
    count = {"Hip-Hop": 0, "International": 0, "Rock": 0, "Experimental": 0, "Electronic": 0,
                "Folk": 0, "Pop": 0, "Instrumental": 0}
    for i, genre in enumerate(predictions):
        if genre == testdf["Class"][i]:
            count[genre] += 1

    # Display results
    print("Total Number of predictions:",len(predictions))

    total = 0
    for k in count.keys():
        total += count[k]
        print("Correct Categorization For {}: {}".format(k, count[k]))

    print("Total Number of correct categorizations: ", total)
    print("Test set accuracy: ", total/len(predictions))

if __name__ == "__main__":
    predict()