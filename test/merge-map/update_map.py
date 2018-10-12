#! /usr/bin/env python

'''To comfort pylint who barks when it can't find a docstring'''

import os
import sys
import time
import argparse
from merge_maps import merge_maps

def get_cur_time_str():
  '''To comfort pylint who barks when it can't find a docstring'''

  seconds_from_1970 = time.time()
  int_seconds = int(seconds_from_1970)
  localtime = time.localtime(int_seconds)
  time_str = '%04d-%02d-%02d_%02d-%02d-%02d_%06d'%(
      localtime.tm_year, localtime.tm_mon, localtime.tm_mday,
      localtime.tm_hour, localtime.tm_min, localtime.tm_sec,
      1000000*(seconds_from_1970-int_seconds))
  return time_str


def parse_arguments(argv):
  '''To comfort pylint who barks when it can't find a docstring'''

  parser = argparse.ArgumentParser(
      description='update vi-map with newly collected data')

  parser.add_argument(
      '--output_vimap_folder', metavar='output_vimap_folder', nargs='?',
      help='folder to the output merged vi-map', required=True)

  parser.add_argument(
      '--vimaps_to_merge', metavar='vimaps_to_merge', nargs='+',
      help='paths to new_vimaps', required=True)

  parser.add_argument(
      '--overwrite', metavar='overwrite', nargs='?', type=bool,
      default=False,
      help='erase existing vi-maps or not (default: %(default)s)',
      required=False)

  parser.add_argument(
      '--vimap_to_anchor_to', metavar='vimap_to_anchor_to', nargs='?',
      help='folder to the vi-map that you want to align the merged map to',
      required=False)

  parser.add_argument(
      '--summary_map_to_anchor_to',
      metavar='summary_map_to_anchor_to', nargs='?',
      help='folder to the summary map that you want to align the merged map to',
      required=False)

  return parser.parse_args(argv)


def get_default_paramset(enable_localization=False, param_class='all'):
  '''To comfort pylint who barks when it can't find a docstring'''

  my_loc = os.path.abspath(os.path.split(__file__)[0])

  loop_closure_paramset = \
      '--lc_projection_matrix_filename=' + my_loc + os.sep + \
      '../../../../devel/share/loopclosure/projection_matrix_brisk.dat '

  loop_closure_paramset = \
      loop_closure_paramset + \
      '--lc_num_words_for_nn_search=30 --lc_min_inlier_ratio=0.15 '\
      '--lc_min_inlier_count=10 --lc_knn_epsilon=0.5 '\
      '--feature_descriptor_type=brisk'
  feature_tracking_paramset = \
      '--swe_feature_tracking_detector_max_feature_count=300 '\
      '--feature_tracking_detector_type=orb '\
      '--swe_feature_tracking_detector_orb_pyramid_levels=2 '\
      '--swe_feature_tracking_detector_orb_scale_factor=1.05 '\
      '--swe_feature_tracking_detector_orb_fast_threshold=15 '\
      '--swe_feature_tracking_detector_orb_patch_size=15'
  if param_class == 'all':
    paramset = feature_tracking_paramset + ' ' + loop_closure_paramset
  elif param_class == 'only_feature_tracking':
    paramset = feature_tracking_paramset
  elif param_class == 'only_loop_closure':
    paramset = loop_closure_paramset
  else:
    paramset = ''

  if enable_localization:
    paramset += ' --localization'
  return paramset


def main(argv):
  '''To comfort pylint who barks when it can't find a docstring'''

  arg = parse_arguments(argv)
  print arg

  if os.path.exists(arg.output_vimap_folder):
    if arg.overwrite:
      os.system("rm -rf "+arg.output_vimap_folder)
      #os.removedirs(arg.output_vimap_folder)
    else:
      print 'WARNING: the specified --output_vimap_folder already exists. '\
            'use --overwrite or choose another folder'
      return 1

  # prepare "vimaps_to_merge"
  vimaps_to_merge = []
  if len(arg.vimaps_to_merge) > 0:
    for vimap in arg.vimaps_to_merge:
      vimaps_to_merge.append(os.path.abspath(vimap))

  if not os.path.exists(arg.output_vimap_folder):
    os.makedirs(arg.output_vimap_folder)
  merge_maps(vimaps_to_merge, "merged_map",
             paramset=get_default_paramset(param_class='only_loop_closure'),
             outputdir=arg.output_vimap_folder,
             summary_map_to_anchor_to=arg.summary_map_to_anchor_to)

  return 0

if __name__ == '__main__':
  exit(main(sys.argv[1:]))
