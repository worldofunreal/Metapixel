import cv2

# Check OpenCV version
print(f"OpenCV Version: {cv2.__version__}")

# Try to open an image (adjust the path to an actual image file)
image_path = "totem1.png"
image = cv2.imread(image_path)

if image is not None:
    print("Image loaded successfully!")
    cv2.imshow("Test Image", image)

    # Wait for the 'q' key to be pressed to exit
    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
else:
    print("Failed to load image.")