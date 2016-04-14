1. unzip AirPrint_Activator.zip
2. mv everything from the zip to C:\Program Files\AirPrint
3. Run cmd
    sc.exe create AirPrint binPath= "C:\Program Files\AirPrint\airprint.exe -R _ipp._tcp,_universal -s" depend= "Bonjour Service" start= auto 
    sc.exe start AirPrint 
