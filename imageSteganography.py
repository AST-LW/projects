# Least significant bit method used for message hidding

import numpy as np  # package for performing martix operations
import math         # package that has math operaions
import matplotlib.pyplot as plt # package for reading and plotting the image

# methods

def color_splitter(image):  # function to split into RGB color gray images
    return [image[:,:,0],image[:,:,1],image[:,:,2]]

def check_bits(string): 
    if len(string)!=8:  # checking whether all the bits are 8-bits if not then add zeros to lhs
        return ((string[::-1]+''.join(['0' for i in range(8-len(string))])))[::-1]
    return string

def changing_bits(num,x):  # this function is used to exchange the bits in image and message and vice versa
    num=check_bits(bin(num).replace('0b',''))    
    temp=num[-1]
    num=int(num[:len(num)-1]+x,2) # after changing convert into decimal number, num[:len(num)-1]+x is in string format
    return num,temp    

def simple_LSB_sourceSide(image,message): # image in np array
    row,column=image.shape
    image=image.tolist()    # converting the 2D matrix to single dimension for easy manipulations 
    if row*column<len(message)*8: # checking size
        return 'Image Size is less than Message'
    data=''
    if len(message)==1: # only one character
        data=check_bits(bin(ord(message)).replace('0b',''))
    else:  # multiple characters
        for char in message: 
            data+=check_bits(str(bin(ord(char)).replace('0b','')))
    len_data=0 
    suppressed_bits=[] # list to maintain the replaced bits
    for i in range(len(image)): 
        if len_data<len(data): # break when message bits are over
            for j in range(len(image[i])): 
                if len_data<len(data):  # break when message bits are over too 
                    image[i][j],temp=changing_bits(image[i][j],data[len_data])
                    len_data+=1
                    suppressed_bits.append(temp)
                else: 
                    break
        else:
            break
    image=np.array(image).reshape(row,column)
    return [image,suppressed_bits] # return image and image bits 

def simple_LSB_destinationSide(image,suppressed_bits):  # apply the same process as above
    row,column=image.shape
    image=image.tolist()
    res=''   # for storing the final Message
    len_suppressed_bits=0
    for i in range(len(image)): 
        if len_suppressed_bits<len(suppressed_bits):
            for j in range(len(image[i])): 
                if len_suppressed_bits<len(suppressed_bits):
                    image[i][j],temp=changing_bits(image[i][j],suppressed_bits[len_suppressed_bits])
                    res+=temp
                    len_suppressed_bits+=1
                else: 
                    break 
        else: 
            break
    start=0
    message=''
    res=list(res)
    while start<len(res):
        message+=chr(int(''.join(res[start:start+8]),2)) # changing the bits to character
        start+=8
    image=np.array(image).reshape(row,column)
    return [image,message]

# quality measures:-

# mean squared error should be as low as possible

def mean_squared_error(original_image,steg_image): # arguments in np.array format
    temp=(original_image-steg_image).tolist()  # original and steg images are np array before converting to list
    sum_=0
    for i in range(len(temp)): 
        for j in range(len(temp[i])): 
            sum_+=temp[i][j]**2
    return float(sum_/(len(temp)*len(temp[0])))
    # return np.mean((original_image-steg_image)**2)
    
def root_mean_squared_error(original_image,steg_image): 
    return math.sqrt(mean_squared_error(original_image,steg_image))

# PSNR should be greater than 58 db for best

def peak_signal_to_noise_ratio(mse,max_fluctuation): # max_fluctuation is max value in image
    return '{} dB'.format(float(10*math.log10(pow(max_fluctuation,2)/mse)))
    
# NCC must be as high as possible 
    
def normalized_cross_correlation(original_image,steg_image):  # input in np array
    sum_numer=0
    sum_denom=0
    temp=original_image.tolist()
    temp_1=(original_image*steg_image).tolist()
    sum_numer=sum([temp_1[i][j] for i in range(len(temp_1)) for j in range(len(temp_1[i]))])
    for i in range(len(temp)): 
        for j in range(len(temp[i])):
                       sum_denom+=pow(temp[i][j],2)
    return float(sum_numer/sum_denom) 
    
def main(image_path): 
    image=plt.imread(image_path)
    gray_image=image[:,:,0]
    lsb_image,lsb_bits=simple_LSB_sourceSide(gray_image,'hello world!!!')
    # plt.imshow(lsb_image,cmap='gray')
    original_image,message=simple_LSB_destinationSide(lsb_image,lsb_bits)
    print('this is the decoded message from lsb of image, '+message)
    print('quality measurements of both steg-image and original image')
    print('MSE: '+str(mean_squared_error(gray_image,lsb_image)))
    print('PNSR (peak signal to noise ratio): '+str(peak_signal_to_noise_ratio(mean_squared_error(gray_image,lsb_image),255)))
    print('NCC (normalized cross correlation): '+str(normalized_cross_correlation(gray_image,lsb_image)))

main('add image path here')
# eg: main('C:/Users/Admin/OneDrive/Desktop/image.jpg')

# outputs:-

# this is the decoded message from lsb of image, hello world!!!
# quality measurements of both steg-image and original image
# MSE: 0.0013083556348498365
# PNSR (peak signal to noise ratio): 76.96354551696358 dB
# NCC (normalized cross correlation): 0.9999988504279365