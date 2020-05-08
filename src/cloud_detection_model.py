"""
    -> Script to train the model from scratch.
    -> command to run:
        python retrain.py\
         --train_dataset=<PATH TO TRAINING DATASET DIRECTORY>\
         --validation_dataset=<PATH TO VALIDATION DATASET DIRECTORY>\
         --training_dir=DIRECTORY TO SAVE TRAINING DATA (CHECKPOINTS, LOG, TENSORBOARD..ETC)\
         --batch_size=BATCH SIZE\
         --epochs=TOTAL NO OF EPOCH\
         --workers=TOTAL WORKERS TO PERFORM PARALLEL TASK FOR DATA GENERATION.\
         --max_queue_size=MAXIMUM QUEUE SIZE TO LOAD DATA.
"""

# importing
import argparse
import os
import sys
import tensorflow as tf

from tensorflow.keras import applications
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

tf.enable_resource_variables()

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--train_dataset", help="path to the training dataset directory",
                    type=str)
parser.add_argument("--validation_dataset", help="path to the validation dataset directory",
                    type=str)
parser.add_argument("--training_dir", help="directory path to save training data",
                    type=str)
parser.add_argument("--image_size", help="resize image to the image_size x image_size",
                    type=int, default=224)
parser.add_argument("--batch_size", help="Total batch size",
                    type=int, default=32)
parser.add_argument("--epochs", help="Total Epochs",
                    type=int, default=100)
parser.add_argument("--workers", help="workers for image data generation",
                    type=int, default=1)
parser.add_argument("--max_queue_size", help="maximum queue size for data generation",
                    type=int, default=20)

args = vars(parser.parse_args())

# making directory structure
try:
    os.mkdir(os.path.join(args['training_dir'], 'frozen_graph'))
    os.mkdir(os.path.join(args['training_dir'], 'checkpoints'))
    os.mkdir(os.path.join(args['training_dir'], 'tensorboard_log'))
except:
    print('Directory not empty')
    sys.exit(0)

img_width, img_height = args['image_size'], args['image_size']

nb_train_samples = len(os.listdir(args['train_dataset']))
nb_validation_samples = len(os.listdir(args['validation_dataset']))

def build_model():
    """
        method to load a pretrained model,
        make last 10 node trainable,
        adding an additional dense node
        and return a model.
    """

    # constructing the model
    model = applications.mobilenet.MobileNet(weights="imagenet", include_top=False,
                                             input_shape=(img_width, img_height, 3),
                                             pooling='avg')

    # make starting few layer non trainable
    for layer in model.layers[:-10]:
        layer.trainable = False

    # Adding custom Layers
    x = model.output
    predictions = Dense(2, activation="softmax")(x)

    # creating the final model
    model = Model(inputs=model.input, outputs=predictions)

    return model

model_final = build_model()

# compile the model
model_final.compile(loss="categorical_crossentropy",
                    optimizer=optimizers.Adam(lr=0.01),
                    metrics=["accuracy"])

# Initiate the train and test generators with data Augumentation
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    fill_mode="nearest",
    zoom_range=0.3,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    rotation_range=180)

validation_datagen = ImageDataGenerator(
    rescale=1. / 255,
    fill_mode="nearest",
    zoom_range=0.3,
    rotation_range=30)

train_generator = train_datagen.flow_from_directory(
    args['train_dataset'],
    # save_to_dir = root_visualizaion_dir,
    target_size=(img_height, img_width),
    batch_size=args['batch_size'],
    class_mode="categorical")

validation_generator = validation_datagen.flow_from_directory(
    args['validation_dataset'],
    target_size=(img_height, img_width),
    class_mode="categorical")

# Save the model according to the conditions
checkpoint = ModelCheckpoint(filepath=os.path.join(args['training_dir'],
                                                   'checkpoints',
                                                   'model_{epoch:05d}_{val_acc:.5f}.h5'),
                             verbose=1,
                             monitor='val_acc',
                             save_weights_only=False,
                             mode='auto',
                             period=1)

tbCallBack = tf.keras.callbacks.TensorBoard(log_dir=os.path.join(args['training_dir'],
                                                                 'tensorboard_log'),
                                            histogram_freq=0,
                                            write_graph=True,
                                            write_images=True)

csv_logger = CSVLogger(os.path.join(args['training_dir'], 'training.log'))

print('Training steps:', int(train_generator.n / args['batch_size']))
print('Validation steps:', int(validation_generator.n / args['batch_size']))

# Train the model
model_final.fit_generator(
    train_generator,
    steps_per_epoch=int(train_generator.n / args['batch_size']),
    epochs=args['epochs'],
    validation_data=validation_generator,
    validation_steps=int(validation_generator.n / args['batch_size']),
    workers=args['workers'],
    max_queue_size=args['max_queue_size'],
    callbacks=[checkpoint, tbCallBack, csv_logger])

model_final.save(os.path.join(args['training_dir'],
                                    'checkpoints',
                                    'final_model.h5'))
tf.keras.experimental.export_saved_model(model_final,
                                         os.path.join(args['training_dir'],
                                                      'frozen_graph'))