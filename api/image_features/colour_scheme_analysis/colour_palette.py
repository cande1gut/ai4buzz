import colorgram
import cv2 as cv
from skimage import io
from PIL import Image
import numpy as np

#from api.image_features.feature_analyzer import FeatureAnalyzer

class ColorSchemeAnalyzer():
    def get_descriptions(self, image):
        """ get color palette of image

        :param image: PIL image object
        :return: dict containing color count and rgb values of colors
        """
        colour_palette = self._get_palette(image, 20) 
        # can swap colorgram with k-means
        #k_means_colour_palette = self._get_palette_k_means(image, 3)
        return self._format_description(colour_palette)

    def _format_description(self, description):
        """ format color palette description data

        :param description: dictionary of color palette data
        :return: formatted dictionary of color palette data
        """
        colors = []
        count = 0
        for color in description:
            if color.proportion > 0.05: # only add colours above the set threshold %

                colors.append(
                    {
                        "red": color.rgb.r,
                        "green": color.rgb.g,
                        "blue": color.rgb.b,
                        "proportion": color.proportion
                    }
                )
                count = count + 1

        return {
            "count": count ,
            "colors": colors
        }

    def _get_palette(self, img, num_colours):
        """
        use colorgram.py to get the 20 most common colours in the image

        :param img: PIL image object
        :param num_colours: number of colours to look for
        :return: colorgram.Color object
        """
        colours = colorgram.extract(img,num_colours)
        return colours

    def _get_palette_k_means(self, img, num_colours):
        """"
        Unused
        Alternative option to colorgram
        """
        image = np.array(img)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        Z = image.reshape((-1,3))
        # convert to np.float32
        Z = np.float32(Z)
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = num_colours
        ret,label,center=cv.kmeans(Z,K,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
        # Now convert back into uint8, and make original image
        centers = np.copy(center)
        center = np.uint8(center)

        return center

'''
if __name__ == "__main__":
    colorSchemeAnalyzer = ColorSchemeAnalyzer()
    test_colours = [[255,201,13], [237,27,36], [0,163,232]]
    print(colorSchemeAnalyzer._get_palette('colour_test.jpg',3))

    print(colorSchemeAnalyzer._get_palette_k_means('colour_test.jpg',3))
    print(test_colours)
'''
