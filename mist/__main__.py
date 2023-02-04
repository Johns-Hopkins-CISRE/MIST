#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""__main__.py: Preprocesses and trains the model as per the config.py file"""

__author__ = "Hudson Liu"
__email__ = "hudsonliu0@gmail.com"

import pickle
import os

from config import *
from project_enums import TrainingModes
from model_trainer import DistributedGUI, ModelTrainer
from preprocessor import PreProcessor


# Preprocesses data
if PREPROCESS_DATA:
    preproc = PreProcessor(PATH)
    preproc.import_and_preprocess()
    preproc.regroup()
    preproc.group_shuffle()
    preproc.split_dataset()
    preproc.save_len()

# Defines training parameters
params = PARAMS
if LOAD_TUNER_PARAMS:
    os.chdir(f"{PATH}data/")
    with open("best_hyperparams.pkl", "rb") as f:
        best_hps = pickle.load(f)
    params.update(best_hps)

# Runs training according to declared training method
match MODE:
    case TrainingModes.PLAIN:
        trainer = ModelTrainer(PATH, EXPORT_DIR, params)
        trainer.basic_train()
    case TrainingModes.DIST:
        trainer = ModelTrainer(PATH, EXPORT_DIR, params)
        trainer.dist_train()
    case TrainingModes.TUNER:
        trainer = ModelTrainer(PATH, EXPORT_DIR, params)
        trainer.tuner_train()
    case TrainingModes.GUI | TrainingModes.DIST_GUI | TrainingModes.TUNER_GUI:
        DistributedGUI(PATH, EXPORT_DIR, MODE)
    case other:
        raise ValueError(f"Variable \"MODE\" is invalid, got val \"{MODE}\"")