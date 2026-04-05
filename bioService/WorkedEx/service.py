import ctypes, os, time
from PIL import Image
workingDirectory = os.getcwd().replace("\\", "/")
dll_path = f"{workingDirectory}/ftrScanAPI.dll"
ftr_lib = ctypes.WinDLL(dll_path)
ftr_lib.ftrScanOpenDevice.restype = ctypes.c_void_p

print("Connecting to FS88...")
device_handle = ftr_lib.ftrScanOpenDevice()

if device_handle:
    print(f"Success! Device handle: {device_handle}")
    width, height = 320, 480
    image_size = width * height 
    buffer = ctypes.create_string_buffer(image_size)
    print("--- Waiting for finger ---")
    while True:
        print("Place finger and press Enter to scan (or Ctrl+C to stop)...", end="\r")
        input()
        result = ftr_lib.ftrScanGetFrame(ctypes.c_void_p(device_handle), buffer, None)
        
        if result == 1:
            print("\nFingerprint captured successfully!")
            img = Image.frombytes('L', (width, height), buffer)
            img.save("fingerprint_capture.bmp")
            break
        else:
            print(f"\nCapture failed (Error {result}). Try adjusting your finger.")
            time.sleep(1)

else:
    print("Failed to open device. Check your USB connection.")