@echo off
set /p nombre=Ingrese su nombre:
echo %nombre%
cd C:\Users\Usuario\Desktop\IA\face-recognition-with-liveness-web-login\face_recognition_and_liveness\face_recognition
python encode_faces.py -i dataset\%nombre% -e encoded_faces.pickle -d cnn
exit


