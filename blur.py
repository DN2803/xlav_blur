import numpy as np
import cv2

# Thêm Gaussian noise: https://pythonexamples.org/python-opencv-add-noise-to-image/
def GaussianNoise(img, stddev): 
    mean = (0,0,0)
    noise = np.zeros(img.shape, np.uint8)

    stddev = (stddev,stddev,stddev)

    # Tạo Gaussian noise ngẫu nhiên
    cv2.randn(noise, mean, stddev)

    # Thêm noise vào ảnh
    noisy_img = cv2.add(img, noise)
    
    return noisy_img


def blur_avarage(img, ksize): 
    """
    averange of kernel 
    agrv: 
    img: source image 
    ksize(int, int): size of kernel 
    return 
    img after apply filter 
    """
    h, w, d = img.shape
    ksize1 = ksize[0] //2
    ksize2 = ksize[1] //2
    result = img.copy()
    for z in range (d):
        for x in range(ksize1, h-ksize1):
            for y in range(ksize2, w-ksize2):
                temp = 0
                for i in range (-ksize1 , ksize1+1):
                    for j in range (-ksize2, ksize2+1):
                        temp+= img[x + i, y + j, z]
                temp = temp/(ksize[0]*ksize[1])
                temp = np.round(temp)
                result[x, y, z] = temp
    return result


def gaussian_kernel(size, sigma = 1):
    size1 = size[0]
    size2 = size[1]
    """Generates a 2D Gaussian kernel."""
    kernel = np.fromfunction(
        lambda x, y: (1/ (2 * np.pi * sigma ** 2)) * 
                     np.exp(-((x - (size1-1)/2)**2 + (y - (size2-1)/2)**2) / (2 * sigma ** 2)),
        (size1, size2)
    )
    return kernel / np.sum(kernel)

def blur_Gaussian(img, ksize, sigma):
    """
    follow: 
    1. caculate Gaussian kernel
    2. convolution image with the kernel
    img: source image in gray scale 
    ksize: size of kernel 
    sigma: standard deviation of gaussian distribution, assumed same for x and y. 

    return 
    img after apply blur filter 
    """
    h, w , d = img.shape
    ksize1 = ksize[0] //2
    ksize2 = ksize[1] //2

    # tính kernel gaussian
    
    H_gaussian = gaussian_kernel(ksize, sigma)
    result = img.copy()

    for z in range(d): 
        for x in range(ksize1, h-ksize1):
            for y in range(ksize2, w-ksize2):
                temp = 0
                for i in range (-ksize1 , ksize1+1):
                    for j in range (-ksize2, ksize2+1):
                        temp +=img[x + i, y + j, z]*H_gaussian[i+ksize1, j+ksize2]
                temp = np.round(temp)
                result[x, y, z] = temp
    return result

#hàm sắp xếp các phần tử
def Sort_array(a):
    flag = False
    for i in range (0, len(a), 1):
        for j in range (0, len(a) - i - 1, 1):
            if(a[j].any() > a[j + 1].any()):
                temp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = temp
                flag = True
        
        if(flag == False):
          break

def get_neighbors(matrix, row, col,deppt,  radius):
    """
    Get the neighbors of a point in a 2D matrix within a given radius.
    
    Parameters:
    - matrix: 2D NumPy array
    - row, col: Coordinates of the point
    - radius: Radius around the point to consider
    
    Returns:
    - neighbors: 1D NumPy array containing the values of the neighboring points
    """
    start_row = max(0, row - radius)
    end_row = min(matrix.shape[0], row + radius +1)
    start_col = max(0, col - radius)
    end_col = min(matrix.shape[1], col + radius +1)
    
    neighbors = matrix[start_row:end_row, start_col:end_col, deppt].flatten()
    return neighbors

def blur_Median(img, ksize):
    """
    follow: 
    for each filter with kernel size get median 
    agrv: 
    img: source image
    ksize (int, int): size of kernel 
    return 
    img after apply blur filter 
    """
    h, w, d = img.shape
    ksize1 = ksize[0] //2
    ksize2 = ksize[1] //2
    size = ksize[0]*ksize[1]

    result = img.copy()
    for z in range (d):
        for x in range (ksize1,h-ksize1):
            for y in range (ksize2,w-ksize2):
                # tạo filter với các điểm lân cận
                members = get_neighbors(img, x, y,z,ksize1)
                members = sorted(members)
                # lấy giá trị trung vị
                med = members[size//2+1]
                result[x, y, z] = med
    return result

