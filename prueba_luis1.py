# -*- coding: utf-8 -*-
"""
- PRUEBA LUIS 1 -

Código de primera aproximación realizada por Luis Osorio para la medición de distancias con OpenCV. Código no utilizado en las mediciones reales. 

Created on Fri Nov 24 13:53:21 2023
@author: CCTVal - LO
"""


import cv2
import numpy as np

def calculate_displacement(prev_frame, current_frame, orb, kp_ref, des_ref, reference_size_mm):
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    kp2, des2 = orb.detectAndCompute(current_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des_ref, des2)

    # Use only the first match
    match = matches[0]

    displacement = match.distance

    # Calibrate displacement using the reference object size
    pixel_to_mm_conversion = reference_size_mm / 137
    calibrated_displacement = displacement * pixel_to_mm_conversion

    return calibrated_displacement, match

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Unable to open video capture.")
        return

    ret, prev_frame = cap.read()
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    kp_ref, des_ref = orb.detectAndCompute(prev_gray, None)

    reference_size_mm = 30.0

    while cap.isOpened():
        ret, current_frame = cap.read()

        if not ret:
            print("Error: Unable to read frame.")
            break

        displacement, match = calculate_displacement(prev_frame, current_frame, orb, kp_ref, des_ref, reference_size_mm)

        # Draw the matched point on the current frame
        img_matches = cv2.drawMatches(prev_frame, kp_ref, current_frame, kp_ref,
                                      [match], None, 
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # Display the matches in real-time
        cv2.imshow("Matches", img_matches)

        # Print displacement
        print("Displacement:", displacement)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
    
    
