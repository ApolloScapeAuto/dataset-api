import cv2
import data
import utils as uts
from collections import OrderedDict


def stereo_rectify_test():
    image_name = 'test/180602_015140124'
    dataset = data.ApolloScape(scale=1.0, use_stereo=True)
    images = OrderedDict([])
    image_size = dataset._data_config['image_size']
    for cam_name in ['Camera_5', 'Camera_6']:
        images[cam_name] = cv2.imread('%s_%s.jpg' % (image_name, cam_name))
        images[cam_name] = cv2.resize(
            images[cam_name], (image_size[1], image_size[0]))
        images[cam_name] = dataset.stereo_rectify(images[cam_name], cam_name)

    for cam_name in ['Camera_5', 'Camera_6']:
        images[cam_name + '_crop'] = uts.crop_image(images[cam_name],
                                                    dataset._data_config['stereo_crop'])

    uts.plot_images(images, layout=[2, 2])


if __name__ == '__main__':
    stereo_rectify_test()
    print('test data pass')
