from PIL import Image
import cv2
import numpy as np



def prepare(image, thresh_low, thesh_type='THRESH_BINARY_INV'):
    gauss = cv2.GaussianBlur(image, (21, 21),  21)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if thesh_type != 'THRESH_BINARY_INV':
        ret, thresh2 = cv2.threshold(gray, thresh_low, 255, cv2.THRESH_BINARY_INV)
    else:
        ret, thresh2 = cv2.threshold(gray, thresh_low, 255, cv2.THRESH_BINARY)
    
    # Less aggressive dilation and erosion
    kernel = np.ones((15, 15), np.uint8)
    dialted= cv2.dilate(thresh2,(7,7),iterations=7)

    eroded = cv2.erode(dialted, kernel, iterations=7)
    
    return eroded

def extract_image_boxes(image, thresh_low=250, thesh_type='THRESH_BINARY'):

    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    processed_image = prepare(opencv_image, thresh_low=thresh_low, thesh_type=thesh_type)
    
    nlabel, labels, stats, centroids = cv2.connectedComponentsWithStats(processed_image, connectivity=8)
    
    extracted_images = []
    
    for i in range(1, nlabel): 
        x, y, w, h, area = stats[i]
        
        component_image = opencv_image[y:y+h, x:x+w]
        
        component_pil_image = Image.fromarray(cv2.cvtColor(component_image, cv2.COLOR_BGR2RGB))
        extracted_images.append(component_pil_image)
    
    return extracted_images
