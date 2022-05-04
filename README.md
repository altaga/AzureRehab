# AzureRehab

Rehabilitation system based on Azure AI and QuickLogic QuickFeather which detects rehabilitation movements and gives feedback to the patient.

<img src="https://i.ibb.co/r780WVz/Azure-Rehab.png">

# Table of contents

- [AzureRehab](#azurerehab)
- [Table of contents](#table-of-contents)
- [Introduction:](#introduction)
- [Materials:](#materials)
- [Connection Diagram:](#connection-diagram)
- [SensiML:](#sensiml)
  - [Sample Examples:](#sample-examples)
  - [Sampling:](#sampling)
  - [Training:](#training)
  - [Model Test: Real Time Labeling:](#model-test-real-time-labeling)
- [Azure TensorFlow Serverless Function:](#azure-tensorflow-serverless-function)
- [Azure VM, MQTT Server:](#azure-vm-mqtt-server)
- [Main UI:](#main-ui)
    - [Our Epic DEMO:](#our-epic-demo)
  - [Future Rollout:](#future-rollout)
  - [References:](#references)

# Introduction:

Rehabilitation system based on Azure AI and [QuickLogic QuickFeather](https://sensiml.com/documentation/firmware/quicklogic-quickfeather/quicklogic-quickfeather.html)

There are people in the world that suffer serious impediments in their arms. These are from several illnesses such as stroke, Guillain-Barré syndrome, paralysis from birth, cerebral palsy, spina bifida, spinal muscular atrophy and several others.
These patients have to continuously take rehabilitation therapies, which are expensive:

The prices of these sessions cost from $ 650 to $ 1300 dollars and sometimes are not insurable:
https://www.healthline.com/health/cool-sculpting-cost

They take a lot of time and it is also necessary to go to specific clinics to receive them, which increases the pain and discomfort of the patient due to the physical effort.

The clinical devices that perform the rehabilitation are enormous and can not be transported or mobilized easily:
https://www.hocoma.com/solutions/armeo-power/
https://www.researchgate.net/figure/Examples-of-robotic-devices-for-motor-training-A-End-effector-type-InMotion-20_fig1_259609214

Therefore we must create a device capable of helping the patient in his rehabilitation, give him continuous feedback of his therapy and it has to be economical (to a certain degree and in comparison to the other choices).

# Materials:

Hardware:
- [QuickFeather Development Kit. 1x.](https://www.quicklogic.com/products/eos-s3/quickfeather-development-kit/)
- [ESP32. 1x](https://www.adafruit.com/product/3405)
- [Robotic Arm x1.](https://www.amazon.com/OWI-Robotic-Soldering-Required-Extensive/dp/B0017OFRCY)
- [ESP32 x1.](https://www.adafruit.com/product/3405)
- [8 Channel DC 5V Relay Module with Optocoupler x1.](https://www.amazon.com/Elegoo-Module-Optocoupler-Arduino-Raspberry/dp/B07F623PHG)

Software:
- [Azure Function App](https://azure.microsoft.com/en-us/services/functions/)
- [Azure VM (MQTT Server)](https://azure.microsoft.com/en-us/services/virtual-machines/)
- [Azure Static Web App](https://azure.microsoft.com/en-us/services/app-service/static/)
- [TensorFlow](https://www.tensorflow.org/)
- [Python Anaconda](https://www.anaconda.com/products/distribution)

# Connection Diagram:

This is the connection diagram of the system:

<img src="https://i.ibb.co/dtRRfrL/Scheme-drawio.png">

# SensiML:

QuickFeather Software: [CLICK HERE](./SensiML%20Project/)

## Sample Examples:

Before performing any other task, it was vital to be able to generate a model for elbow rehabilitation, the system can be extended to any rehabilitation but we chose elbow as the first sample.

4 basic movements were programmed for the rehabilitation of the elbow, of which 3 of them will be used in the final rehabilitation.

Elbow flexoextension:

<img src="https://i.ibb.co/qkX5VfF/image.png" width="400">
<img src="https://i.ibb.co/RBY7K7L/image.png" width="400">

Arm Lift:

<img src="https://i.ibb.co/CzXGq2v/image.png" width="400">
<img src="https://i.ibb.co/XZdHHrS/image.png" width="400">

Elbow Flexion:

<img src="https://i.ibb.co/jkJ4qfd/image.png" width="400">
<img src="https://i.ibb.co/hDrN088/image.png" width="400">

## Sampling:

This is the model that was developed and the number of repetitions for each movement:

<img src="https://i.ibb.co/tqD3zcC/image.png">

## Training:

Classifier Algorithm:

<img src="https://i.ibb.co/MGV5rp4/image.png">

Model motion confusion matrix:

<img src="https://i.ibb.co/FJ6f79B/image.png">

## Model Test: Real Time Labeling:

Elbow flexo-extension:

<img src="./Images/Gifs/efe.gif">

Arm Lift (Lateral raise):

<img src="./Images/Gifs/al.gif">

Elbow Flexion:

<img src="./Images/Gifs/ef.gif">

# Azure TensorFlow Serverless Function:

Function Files: [CLICK HERE](./TF-FunctionApp/)

Para poder crear la funcion y poder testearla en un ambiente local, se decidio utilizar la extension de Azure para VScode.

<img src="https://i.ibb.co/SxxnJwH/image.png">

Y para configurar la version correcta de python en la computadora y poder testear correctamente la funcion con el mismo python de la cloud se configuro un environment con Anaconda.

<img src="https://i.ibb.co/DbDFg2h/image.png">

La funcion funciona gracias a un interpreter de Tflite con el fin de optimizar la velocidad de procesamiento de la imagen.

    from tflite_runtime.interpreter import Interpreter
    import azure.functions as func
    import time
    import cv2
    import numpy as np
    import base64

    interpreter = Interpreter("Azure-TFlite/model.tflite")
    interpreter.allocate_tensors()

Y para poder consumirlo mediante API se configuro CORS para permitir a nuestra pagina o nuestro software.

<img src="https://i.ibb.co/FgWkrHW/image.png">

Puedes probar nuestra API desde nuestra pagina web desplegada en Azure Static Web App service.

APP URL:
https://kind-smoke-0ae539610.1.azurestaticapps.net/

Instructions:

- Abre la pagina web.
- Permite el acceso a la camara.
- Si deseas alejarte de la camara puedes apretar el boton de Delay y eso te dara unos segundos adicionales antes de la foto.
- Una vez estes listo presiona el boton de Capture, si tenias algo de delay activo empezara un countdown, sino la foto se tomara de forma instantanea.

EXAMPLE:
<img src="./Images/Gifs/webpage.gif">

# Azure VM, MQTT Server:

La maquina virtual creada para hacer de MQTT server tiene las siguientes caracteristicas.

- Operating system: Linux (ubuntu 20.04)
- Size: Standard B1ls
- Disk: 64Gb

Para gestionar el servicio de MQTT se uso el software [Mosquitto](https://mosquitto.org/), todo se configuro a travez de una terminal de Putty SSH.

<img src="https://i.ibb.co/MBR62Ld/image.png">

El uso principal del servicio MQTT es el control del brazo robotico de forma inalambrica, el controlador del brazo es un ESP32 y un arreglo de 8 Relays.

ARM Software: [CLICK HERE](./ARM-MQTT/)

Arm I/O Connection Diagram:

<img src="https://hackster.imgix.net/uploads/attachments/942233/68747470733a2f2f692e6962622e636f2f4832344451384e2f41524d2d62622e706e67.png" width="400px">

Segun el ejercicio que queremos mostrar tendremos que mandar un mensaje a los siguientes topics.

- /efe

<img src="./Images/Gifs/efebrazo.gif">

- /al

<img src="./Images/Gifs/albrazo.gif">

- /ef

<img src="./Images/Gifs/efbrazo.gif">

# Main UI:

Combinando todos los elementos anteriores se programo una UI sencilla para el medico terapeuta, con el fin de que pueda controlar el brazo a distancia, recibir los datos del QuickFeather y a su vez ver la pose del paciente.

<img src="https://i.ibb.co/M9DnTxr/vlcsnap-2022-05-03-18h39m17s445.png">

Tkinter UI:

UI Files: [CLICK HERE](./TkinterUI/)

Esta UI esta echa en Python y permite controlar con los 3 botones inferiores que ejercicio va a mostrar el brazo al paciente, a su vez de mostrar la imagen procesada por la AI.

<img src="https://i.ibb.co/31Lnyq8/vlcsnap-2022-05-03-18h39m17s445-1.png">

### Our Epic DEMO:

Video: Click on the image
[![Rehab](https://i.ibb.co/r780WVz/Azure-Rehab.png)](PENDING)

Sorry github does not allow embed videos.

## Future Rollout:



## References:

Links 