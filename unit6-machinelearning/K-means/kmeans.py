import urllib.request
import io
import random
import time
import sys
from PIL import Image

#img = Image.open("nature.jpeg")

def color_27_quantization(img):
    new_img = img.copy()
    width, height = new_img.size
    new_pix = new_img.load() 
    for i in range(width):
        for j in range(height):
            colors = new_pix[i, j]
            new_colors = []
            for value in colors:
                if value < (255 // 3):
                    new_colors.append(0)
                elif value > (255 * 2 // 3):
                    new_colors.append(255)
                else:
                    new_colors.append(127)
            new_pix[i, j] = (new_colors[0], new_colors[1], new_colors[2])
    new_img.show()
    new_img.save("27naive_nature.png")

def color_8_quantization(img):
    new_img = img.copy()
    width, height = new_img.size
    new_pix = new_img.load() 
    for i in range(width):
        for j in range(height):
            colors = new_pix[i, j]
            new_colors = []
            for value in colors:
                if value < 128:
                    new_colors.append(0)
                else:
                    new_colors.append(255)
            new_pix[i, j] = (new_colors[0], new_colors[1], new_colors[2])
    new_img.show()
    new_img.save("8naive_nature.png")

def create_dict(pix, width, height):
    colors = dict()
    for i in range(width):
        for j in range(height):
            if pix[i, j] in colors.keys():
                colors[pix[i, j]].append((i, j))
            else:
                colors[pix[i, j]] = [(i, j)]
    return colors

def k_means(img):
    new_img = img.copy()
    width, height = new_img.size
    new_pix = new_img.load() 
    means = list()
    colors = create_dict(new_pix, width, height)
    possible_x_values = [num for num in range(img.size[0])]
    possible_y_values = [num for num in range(img.size[1])]
    while len(means) < k_value:
        x_value = random.choice(possible_x_values)
        y_value = random.choice(possible_y_values)
        if new_pix[x_value, y_value] not in means:
            means.append(new_pix[x_value, y_value])
    mean_pixels = [[] for i in range(k_value)]
    generation = 0
    #loop over dictionary keys
    for color in colors.keys():
        color_distance, cur_mean, mean_index = min([(distance(mean, color), mean, index) for index, mean in enumerate(means)], key=lambda x: x[0])
        new_pixels = colors[color].copy()
        mean_pixels[mean_index].extend(new_pixels)    
    generation += 1
    new_means = list()
    for m in range(len(means)):
        average_tuple = find_average(new_pix, mean_pixels[m])
        new_means.append(average_tuple)
    new_mean_pixels = [[] for i in range(k_value)] 
    for color in colors.keys():
        color_distance, cur_mean, mean_index = min([(distance(mean, color), mean, index) for index, mean in enumerate(new_means)], key=lambda x: x[0])
        new_mean_pixels[mean_index].extend(colors[color])    
    difference_list = [len(new_mean_pixels[j]) - len(mean_pixels[j]) for j in range(len(means))]
    print(f'Generation {generation}: {difference_list}')
    means = new_means
    mean_pixels = new_mean_pixels 
    while not all(v == 0 for v in difference_list):
        generation += 1
        new_means = list()
        for m in range(len(means)):
            average_tuple = find_average(new_pix, mean_pixels[m])
            new_means.append(average_tuple)
        new_mean_pixels = [[] for i in range(k_value)] 
        for color in colors.keys():
            color_distance, cur_mean, mean_index = min([(distance(mean, color), mean, index) for index, mean in enumerate(new_means)], key=lambda x: x[0])
            new_mean_pixels[mean_index].extend(colors[color])
        difference_list = [len(new_mean_pixels[j]) - len(mean_pixels[j]) for j in range(len(means))]
        print(f'Generation {generation}: {difference_list}')
        means = new_means
        mean_pixels = new_mean_pixels 
    for count, mean in enumerate(means):
        for pixel in mean_pixels[count]:
            new_pix[pixel[0], pixel[1]] = (round(mean[0]), round(mean[1]), round(mean[2]))
    #new_img.show()
    new_img.save('kmeansout.png')

def distance(pixel1, pixel2):
    red = (pixel1[0] - pixel2[0]) ** 2
    blue = (pixel1[1] - pixel2[1]) ** 2
    green = (pixel1[2] - pixel2[2]) ** 2
    return red + blue + green

def find_average(new_pix, pixels):
    red_sum = 0
    blue_sum = 0
    green_sum = 0
    for i in range(len(pixels)):
        red_sum += new_pix[pixels[i][0], pixels[i][1]][0]
        green_sum += new_pix[pixels[i][0], pixels[i][1]][1]
        blue_sum += new_pix[pixels[i][0], pixels[i][1]][2]
    avg_tuple = (red_sum/len(pixels), green_sum/len(pixels), blue_sum/len(pixels))
    return avg_tuple

URL = sys.argv[1]
f = io.BytesIO(urllib.request.urlopen(URL).read())
img = Image.open(f)
k_value = int(sys.argv[2])
start = time.perf_counter()
k_means(img)
end = time.perf_counter()
print(f'Time: {end - start}')