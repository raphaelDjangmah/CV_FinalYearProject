import cv2
from skimage.metrics import structural_similarity as ssim

class Algorithms:

    def ssimChecker(self, path1:str, path2:str):
        img1,img2 = None, None

        try:
            img1 = cv2.imread(path1)
            img2 = cv2.imread(path2)
        except:
            return -1

        #write image correctly
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        #convert the images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

        # Ensure both images have the same dimensions
        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))

        #check color difference between images
        ssim_score = ssim(gray1, gray2)
        return ssim_score
    
    def siftChecker(self, path1:str, path2:str):
        img1,img2 = None, None

        try:
            img1 = cv2.imread(path1)
            img2 = cv2.imread(path2)
        except:
            return -1
        
        #write image correctly
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        #convert the images to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

        #sift
        sift = cv2.SIFT_create()

        # Extract SIFT keypoints and descriptors for the objects
        kp1, des1 = sift.detectAndCompute(gray1, None)
        kp2, des2 = sift.detectAndCompute(gray2, None)

        # Create a FLANN matcher
        flann = cv2.FlannBasedMatcher()

        # Match the descriptors of the objects
        matches = flann.knnMatch(des1, des2, k=2)

        #-------------------------------------------------------------------------------------
        # Apply Lowe's ratio test to filter good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

        #compare with other good matches
        benchMarkMatches = []
        for m, n in matches:
            if m.distance < 0.9 * n.distance:
                benchMarkMatches.append(m)

        simRatio = float(len(good_matches)/len(benchMarkMatches))
        
        return simRatio
        


        
