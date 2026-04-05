import ctypes, os, base64

workingDir = os.getcwd()
scanAPI = ctypes.WinDLL(os.path.join(workingDir, "ftrScanAPI.dll"))
ftrAPI = ctypes.WinDLL(os.path.join(workingDir, "FTRAPI.dll"))

class ServiceForTemplate:
    successCode = 1

    def getTemplate():
        handleDevice = scanAPI.ftrScanOpenDevice()
        if not handleDevice:
            print("Device not found")
            return None

        width, height = 320, 480
        imageSize = width * height
        imageBuffer = ctypes.create_string_buffer(imageSize)

        print("Place finger and press Enter...")
        input()

        result = scanAPI.ftrScanGetFrame(ctypes.c_void_p(handleDevice), imageBuffer, None)

        if result == ServiceForTemplate.successCode:
            tmpBuffer = ctypes.create_string_buffer(2048)
            tmpSize = ctypes.c_int(0)
            try:
                res = ftrAPI.ftrEnroll(ctypes.c_void_p(handleDevice), imageBuffer, tmpBuffer, ctypes.byref(tmpSize))
                if res == 0:
                    b64Template = base64.b64encode(tmpBuffer[:tmpSize.value]).decode('utf-8')
                    print("Template created successfully!")
                    return b64Template
                else:
                    print(f"Enrollment failed with error: {res}")
            except AttributeError:
                print("Function 'ftrEnroll' not found in FTRAPI.dll. Try 'ftrCreateTemplate'.")
                
        scanAPI.ftrScanCloseDevice(ctypes.c_void_p(handleDevice))
        return None


myTmp = ServiceForTemplate.getTemplate()
if myTmp:
    print(f"Your Database Template: {myTmp[:60]}...")