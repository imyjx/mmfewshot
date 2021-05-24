import copy
from unittest.mock import MagicMock, patch

import numpy as np

from mmfewshot.detection.datasets import FewShotCustomDataset

data_infos = [
    {
        'id': '1',
        'filename': 'tests/data/VOCdevkit/VOC2007/JPEGImages/000001.jpg',
        'width': 800,
        'height': 720,
        'ann': {
            'bboxes': np.array([[10, 10, 100, 100], [20, 20, 200, 200]]),
            'labels': np.array([0, 1])
        }
    },
    {
        'id': '2',
        'filename': 'tests/data/VOCdevkit/VOC2007/JPEGImages/000002.jpg',
        'width': 800,
        'height': 720,
        'ann': {
            'bboxes': np.array([[11, 11, 100, 100], [20, 20, 200, 200]]),
            'labels': np.array([1, 1])
        }
    },
    {
        'id': '3',
        'filename': 'tests/data/VOCdevkit/VOC2007/JPEGImages/000003.jpg',
        'width': 800,
        'height': 720,
        'ann': {
            'bboxes':
            np.array([[11, 11, 100, 100], [20, 20, 200, 200],
                      [20, 20, 200, 200]]),
            'labels':
            np.array([2, 3, 3, 4])
        }
    },
    {
        'id': '4',
        'filename': 'tests/data/VOCdevkit/VOC2007/JPEGImages/000004.jpg',
        'width': 800,
        'height': 720,
        'ann': {
            'bboxes':
            np.array([[11, 11, 100, 100], [20, 20, 200, 200],
                      [20, 20, 200, 200], [20, 20, 200, 200]]),
            'labels':
            np.array([2, 2, 4, 4])
        }
    },
]


@patch('mmfewshot.detection.datasets.FewShotCustomDataset.load_annotations',
       MagicMock(return_value=data_infos))
def test_few_shot_custom_dataset():
    dataconfig = {
        'ann_file': '',
        'img_prefix': '',
        'ann_shot_filter': {
            'cat': 10,
            'dog': 10,
            'person': 2,
            'car': 2,
        },
        'pipeline': {
            'query': [{
                'type': 'LoadImageFromFile'
            }],
            'support': [{
                'type': 'LoadImageFromFile'
            }]
        },
        'classes': ('cat', 'dog', 'person', 'car', 'bird')
    }

    few_shot_custom_dataset = FewShotCustomDataset(**dataconfig)
    original_data_infos = copy.deepcopy(few_shot_custom_dataset.data_infos)

    # test prepare_train_img()
    data = few_shot_custom_dataset.prepare_train_img(0, 'query')
    assert (data['img_info']['ann']['bboxes'] == np.array([[10, 10, 100, 100],
                                                           [20, 20, 200,
                                                            200]])).all()
    assert (data['img_info']['ann']['labels'] == np.array([0, 1])).all()

    data = few_shot_custom_dataset.prepare_train_img(1, 'support')
    assert (data['img_info']['ann']['bboxes'] == np.array([[11, 11, 100, 100],
                                                           [20, 20, 200,
                                                            200]])).all()
    assert (data['img_info']['ann']['labels'] == np.array([1, 1])).all()

    data = few_shot_custom_dataset.prepare_train_img(0, 'query', [0])
    assert (data['img_info']['ann']['bboxes'] == np.array([[10, 10, 100,
                                                            100]])).all()
    assert (data['img_info']['ann']['labels'] == np.array([0])).all()

    data = few_shot_custom_dataset.prepare_train_img(0, 'support', [1])
    assert (data['img_info']['ann']['bboxes'] == np.array([[20, 20, 200,
                                                            200]])).all()
    assert (data['img_info']['ann']['labels'] == np.array([1])).all()

    # test whether data_infos have been accidentally changed or not
    for i in range(len(few_shot_custom_dataset)):
        assert (original_data_infos[i]['ann']['bboxes'] ==
                few_shot_custom_dataset.data_infos[i]['ann']['bboxes']).all()
        assert (original_data_infos[i]['ann']['labels'] ==
                few_shot_custom_dataset.data_infos[i]['ann']['labels']).all()
