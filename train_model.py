import keras
import os

from segmentation_models import Unet
from keras.layers import Input, Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.models import Model

from keras.callbacks import ModelCheckpoint
from keras.callbacks import CSVLogger
from keras.callbacks import EarlyStopping
from keras.optimizers import Adam

from segmentation_models import Unet
from keras.layers import Input, Conv2D
from keras.models import Model

from segmentation_models.losses import bce_jaccard_loss, dice_loss
from segmentation_models.metrics import iou_score

from data import *

def train_model(batch, data_path, train_raster_file_folder_name, val_raster_file_folder_name, train_mask_file_folder_name, val_mask_file_folder_name, image_color_mode, mask_color_mode, model_weight_path, model_version, number_of_channel, log):
    
    # read/scale/preprocess data
    data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                    fill_mode='nearest')
    myGene_train = trainGenerator(batch,data_path,train_raster_file_folder_name,train_mask_file_folder_name,data_gen_args,image_color_mode =image_color_mode, mask_color_mode = mask_color_mode, save_to_dir = None)
    
    myGene_val = trainGenerator(batch,data_path, val_raster_file_folder_name, val_mask_file_folder_name,data_gen_args,image_color_mode =image_color_mode, mask_color_mode = mask_color_mode, save_to_dir = None)
    
    # define number of channels
    N = int(number_of_channel)

    base_model = Unet(backbone_name='resnet34', encoder_weights='imagenet')

    inp = Input(shape=(None, None, N))
    l1 = Conv2D(3, (1, 1))(inp) # map N channels data to 3 channels
    out = base_model(l1)

    model = Model(inp, out, name=base_model.name)

    opt = Adam(lr=1E-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    model.compile(opt, loss=bce_jaccard_loss, metrics=[iou_score,'accuracy'])

#     checkpoint = ModelCheckpoint(weights_path, monitor='val_loss', 
#                                  verbose=1, save_best_only=True, mode='max')
    # checkpoint
    filepath="weights-improvement-{epoch:02d}-{val_iou_score:.2f}.h5"
    checkpoint = ModelCheckpoint(os.path.join(model_weight_path,filepath), monitor='val_iou_score', verbose=1, save_best_only=True, mode='max')

    csv_logger = CSVLogger(os.path.join(log,'log_{}.out'.format(model_version)), append=True, separator=';')

    earlystopping = EarlyStopping(monitor = 'iou_score', verbose = 1,
                                  min_delta = 0.01, patience = 3, mode = 'max')

    callbacks_list = [checkpoint, csv_logger, earlystopping]

    results = model.fit_generator(myGene_train,steps_per_epoch=2000, validation_data=myGene_val, validation_steps=500, use_multiprocessing=True,workers=4, epochs=5,callbacks=callbacks_list)
    
    model.save(os.path.join(model_weight_path,'Model_unet_{}.h5'.format(model_version)))
    
if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Unet to detect Waters.')
    
    parser.add_argument('--batch', required=False,
                        metavar=4,
                        help='number of batch')
    parser.add_argument('--data_path', required=True,
                        default='/home/ubuntu/sukh_share/water_detection_model/grayscale',
                        metavar="/home/ubuntu/sukh_share/water_detection_model/grayscale",
                        help="root path which contains the dataset")
    parser.add_argument('--train_raster_file_folder_name', required=False,
                        default='train',
                        metavar="train",
                        help='contains original tif files for training')
    parser.add_argument('--train_mask_file_folder_name', required=False,
                        default='train_mask',
                        metavar="train_mask",
                        help='contains mask tif files for training')
    parser.add_argument('--val_raster_file_folder_name', required=False,
                        default='train',
                        metavar="train",
                        help='contains original tif files for validation')
    parser.add_argument('--val_mask_file_folder_name', required=False,
                        default='train_mask',
                        metavar="train_mask",
                        help='contains mask tif files for validation')
    parser.add_argument('--image_color_mode', required=False,
                        default='grayscale',
                        help='color mode which will be used to create the datagenerator for original file')
    parser.add_argument('--mask_color_mode', required=False,
                        default='grayscale',
                        help='color mode which will be used to create the datagenerator for mask')
    parser.add_argument('--model_weight_path', required=False,
                        default='/home/ubuntu/sukh_share/water_detection_model/model_weights',
                        help='path to save the model')
    parser.add_argument('--model_version', required=False,
                        default=0,
                        help='version of the model for a particular mode')
    parser.add_argument('--number_of_channel', required=False,
                        default=1,
                        help='number of channels to be used for the training')
    parser.add_argument('--log', required=False,
                        default='/home/ubuntu/sukh_share/water_detection_model/log',
                        help='number of channels to be used for the training')
    args = parser.parse_args()
    
    
    #start training the model
    train_model(batch=int(args.batch), data_path=args.data_path, train_raster_file_folder_name=args.train_raster_file_folder_name, train_mask_file_folder_name=args.train_mask_file_folder_name, val_raster_file_folder_name=args.val_raster_file_folder_name, val_mask_file_folder_name=args.val_mask_file_folder_name, image_color_mode=args.image_color_mode, mask_color_mode=args.mask_color_mode, model_weight_path=args.model_weight_path, model_version=int(args.model_version), number_of_channel=int(args.number_of_channel),log=args.log)