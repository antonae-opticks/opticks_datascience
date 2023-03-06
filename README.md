# opticks_datascience

The code is organized as follows:
```
├── categoricaldata - Categorical data methodologies
│   ├── hns - Implementation of HNS 
│   └── hnsSvmClassifier - Implementation of HnsSvm classifier 
├── code_base - several low-level features, like parsers, cleaners/var preprocessors, etc.
├── db_access - features for accessing the data from our warehouse. Basically, a json parser
├── ensemble_prototype - the prototypes of the ensemble service. All the docker package.
│   ├── v1
│   │   └── code
│   └── v2
│       └── code
├── gt - code for working with/the ground truth
│   └── coverage - computing the coverage of the GT
└── modules - the ML modules classes 
    ├── clients - client codes
    │   ├── buildWholeHns - client to pre-build a whole HNS instantiation (i.e. to populate cached distributions dictionaries) from a dataset
    │   └── processRf - client to perform a dectection using a trained RF module
    ├── ensemble - the class for the ensemble
    ├── experimental - experimental modules not yet consolidated or discarded
    ├── expertrules - module for the expert rules. Ancient version 
    ├── expertrules_lite - module for the expert rules lite. Modern version using methods detected from the json struct.
    ├── hnssvm - Hns-Svm module class code
    ├── pipeline - pipelines ready to perform tasks
    │   └── train - clients/scripts to train consolidated modules
    │       ├── module_hnssvm
    │       └── module_rf
    ├── preprocessor - data preprocessing module, used by ML modules
    └── rf - random forest module class code
```
