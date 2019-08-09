import os
import logging
from hddl_l_sw_validation.common.utils import _root_no_password, BASE_DIR

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s [%(threadName)s] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


class Sample(object):

    def __init__(self, source_dir):
        """"""
        if source_dir is None:
            raise ValueError('Sample Source DIR not is None')
        if not os.path.exists(source_dir):
            raise ValueError('Sample Source DIR not exists.')
        self.source_dir = source_dir

        self._compile()

    def _compile(self):
        cur_dir = os.getcwd()
        # install_prerequisites
        os.chdir(os.path.join(self.source_dir, 'install_prerequisites'))
        _root_no_password('./install_opencl.sh')
        _root_no_password('./install_opencv.sh')
        # mkdir build
        os.system('mkdir build')
        # compile
        os.chdir(os.path.join(self.source_dir, 'build'))
        os.system('cmake ..')
        os.system('make -j`nproc`')
        os.chdir(cur_dir)

    def run_cross_road(self):
        cur_dir = os.getcwd()
        os.chdir(os.path.join(self.source_dir, 'cross_road_demo'))
        cross_road_demo = '../build/cross_road_demo/cross_road_demo'
        cross_road_demo_dir =os.path.join(BASE_DIR, 'source_cpp/samples/cross_road')

        irs_dir = os.path.join(cross_road_demo_dir, 'irs')
        det_model_path = os.path.join(irs_dir, "pedestrian-and-vehicle-detector-adas-0001-fp16.xml")
        lpr_model_path = os.path.join(irs_dir, "license-plate-recognition-barrier-0001-fp16.xml")
        svm_model_path = os.path.join(irs_dir, "svm_model.xml")

        videos_dir = os.path.join(cross_road_demo_dir, 'videos')
        videos_list = ['cross_road_1_internaldoc_.avi', 'cross_road_2_internaldoc_.avi',
                       'cross_road_3_internaldoc_.avi']
        videos_path = [os.path.join(videos_dir, video_path) for video_path in videos_list]
        cmd = '{} -lm {} -dm {} -svm {} -ddm HDDL -dlm HDDL -v {}'.format(cross_road_demo,
                                                                          lpr_model_path,
                                                                          det_model_path,
                                                                          svm_model_path,
                                                                          ' '.join(videos_path))
        LOGGER.debug('{}'.format(cmd))
        os.system(cmd)
        os.chdir(cur_dir)


if __name__ == '__main__':
    s = Sample(None)
    print(os.getcwd())
    s.run_cross_road()
