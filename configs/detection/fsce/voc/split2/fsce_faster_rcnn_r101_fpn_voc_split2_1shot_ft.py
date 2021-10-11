_base_ = [
    '../../../_base_/datasets/finetune_based/few_shot_voc.py',
    '../../../_base_/schedules/schedule.py',
    '../../fsce_faster_rcnn_r101_fpn.py', '../../../_base_/default_runtime.py'
]
# classes splits are predefined in FewShotVOCDataset
# FewShotVOCDefaultDataset predefine ann_cfg for model reproducibility.
data = dict(
    train=dict(
        type='FewShotVOCDefaultDataset',
        ann_cfg=[dict(method='FSCE', setting='SPLIT2_1SHOT')],
        num_novel_shots=1,
        num_base_shots=1,
        classes='ALL_CLASSES_SPLIT2'),
    val=dict(classes='ALL_CLASSES_SPLIT2'),
    test=dict(classes='ALL_CLASSES_SPLIT2'))
evaluation = dict(
    interval=1500,
    class_splits=['BASE_CLASSES_SPLIT2', 'NOVEL_CLASSES_SPLIT2'])
checkpoint_config = dict(interval=1500)
optimizer = dict(lr=0.001)
lr_config = dict(
    warmup_iters=20, step=[
        2000,
    ])
runner = dict(max_iters=3000)
# load_from = 'path of base training model'
load_from = \
    'work_dirs/' \
    'fsce_faster_rcnn_r101_fpn_voc_split2_base_training/' \
    'model_reset_randinit.pth'
model = dict(frozen_parameters=[
    'backbone', 'neck', 'rpn_head', 'roi_head.bbox_head.shared_fcs.0'
])