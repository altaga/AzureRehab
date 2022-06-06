# AzureRehab

Rehabilitation system based on Azure AI and QuickLogic QuickFeather which detects rehabilitation movements and gives feedback to the patient.

<img src="https://i.ibb.co/r780WVz/Azure-Rehab.png" width="400">


# Introduction:

Welcome to Azure Rehab, a Rehabilitation system based on the [QuickLogic QuickFeather](https://sensiml.com/documentation/firmware/quicklogic-quickfeather/quicklogic-quickfeather.html) which detects rehabilitation movements and gives feedback to the patient through Azure's AI services.

According to the 2019 Global Burden of Disease Study, 2.41 billion individuals, which equates to approximately 1 in 3 people, had conditions that would benefit from rehabilitation.

https://www.physio-pedia.com/Rehabilitation_Global_Needs#:~:text=According%20to%20the%202019%20Global,that%20would%20benefit%20from%20rehabilitation.

Among these there is a huge population that needs arm rehabilitation. These are from several illnesses such as stroke, Guillain-Barré syndrome, paralysis from birth, cerebral palsy, spina bifida, spinal muscular atrophy and several others.
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

- Our edge device communicates through local TCP/IP with the capture lab, this allows us to visualize the predictions of the machine learning model in real time without delays.
- Our Azure Function has the function of performing image processing to predict the position of the person, this API is consumed both in our sample web page and in the Demo Desktop App
- The Azure Static Website service is used for internet deployment of our sample website.
- The virtual machine serves as an MQTT server, which allows us to quickly communicate between the Desktop App and the robot arm.
- All the pertinent results and information is sent then to an Azure CosmosDB to further processing in ML and future reference.

# SensiML:

QuickFeather Software: [CLICK HERE](./SensiML%20Project/)

## Sample Examples:

Before performing any other task, it was vital to be able to generate a model for elbow rehabilitation, the system can be extended to any rehabilitation but we chose elbow as the first sample.

4 basic movements were programmed for the rehabilitation of the elbow, of which 3 of them will be used in the final rehabilitation.

Elbow flexoextension:

<img src="https://i.ibb.co/GM5Qx1B/image-7.png">

Arm Lift:

<img src="https://i.ibb.co/GpVdLdh/image-9.png">

Elbow Flexion:

<img src="https://i.ibb.co/6Fn6FmT/image-8.png">

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

In order to create the function and be able to test it in a local environment, it was decided to use the Azure extension for VScode.

<img src="https://i.ibb.co/SxxnJwH/image.png">

And to configure the correct version of python on the computer and to be able to correctly test the function with the same python from the cloud, an environment with Anaconda was configured.

<img src="https://i.ibb.co/DbDFg2h/image.png">

The function works thanks to a Tflite interpreter in order to optimize the speed of image processing.

    from tflite_runtime.interpreter import Interpreter
    import azure.functions as func
    import time
    import cv2
    import numpy as np
    import base64

    interpreter = Interpreter("Azure-TFlite/model.tflite")
    interpreter.allocate_tensors()

And to be able to consume it through API, CORS was configured to allow our page or our software.

<img src="https://i.ibb.co/FgWkrHW/image.png">

# WebPage DEMO:

You can test our API from our website deployed in Azure Static Web App service.

APP URL:
https://kind-smoke-0ae539610.1.azurestaticapps.net/

Instructions:

- Open the web page.
- Allow camera access.
- If you want to move away from the camera you can press the Delay button and that will give you a few extra seconds before the photo.
- Once you are ready press the Capture button, if you had some active delay a countdown will start, otherwise the photo will be taken instantly.

EXAMPLE:
<img src="./Images/Gifs/webpage.gif">

# Azure VM, MQTT Server:

The virtual machine created to act as MQTT server has the following characteristics.

- Operating system: Linux (ubuntu 20.04)
- Size: Standard B1ls
- Disk: 64Gb

To manage the MQTT service, the [Mosquitto](https://mosquitto.org/) software. Everything was configured through a Putty SSH terminal.

<img src="https://i.ibb.co/MBR62Ld/image.png">

The main use of the MQTT service is to control the robotic arm wirelessly, the arm controller is an ESP32 and an array of 8 Relays.

ARM Software: [CLICK HERE](./ARM-MQTT/)

Arm I/O Connection Diagram:

<img src="https://hackster.imgix.net/uploads/attachments/942233/68747470733a2f2f692e6962622e636f2f4832344451384e2f41524d2d62622e706e67.png" width="400px">

Depending on the exercise we want to show, we will have to send a message to the following topics.

- /efe

<img src="./Images/Gifs/efebrazo.gif">

- /al

<img src="./Images/Gifs/albrazo.gif">

- /ef

<img src="./Images/Gifs/efbrazo.gif">

# Main UI:

Combining all the previous elements, a simple UI was programmed for the therapist, so that he can control the arm remotely, receive the data from the QuickFeather and in turn see the patient's pose.

<img src="https://i.ibb.co/M9DnTxr/vlcsnap-2022-05-03-18h39m17s445.png">

Tkinter UI:

UI Files: [CLICK HERE](./TkinterUI/)

This UI is made in Python and allows you to control with the 3 lower buttons which exercise will show the arm to the patient, in turn showing the image processed by the AI.

<img src="https://i.ibb.co/31Lnyq8/vlcsnap-2022-05-03-18h39m17s445-1.png" width="400">

# Prototypes:

## FPGA Device:
<img src="https://i.ibb.co/5LzCSKF/20220515-234222-001-1.png" width="400">
<img src="https://i.ibb.co/rZgd270/20220515-234256-001-1-1.png" width="400">

### Final:

<img src="https://i.ibb.co/0sCbL5j/20220515-234112-1.png" width="400">

## Robot Arm:
<img src="https://i.ibb.co/s1hZHWx/20220515-234035-1.png" width="400">
<img src="https://i.ibb.co/CVdmmTS/20220515-234407-1.png" width="400">

### Final:
<img src="https://i.ibb.co/rx5Qpty/vlcsnap-2022-05-15-16h09m04s778.png" width="400">

## Full Solution:
<img src="https://i.ibb.co/Wvs7Vhk/image-6-1.png" width="400">

# Our DEMO:

Video: Click on the image
[![Rehab](https://i.ibb.co/r780WVz/Azure-Rehab.png)](PENDING)

Sorry github does not allow embed videos.

# Business Opportunity
The global rehabilitation equipment market is set to grow and keep growing at an alarming rate. The reasons for this are the increasing number of disabilities that are derived from non-communicable diseases, favorable reforms in the healthcare sector and an increasing geriatric population coupled with increasing incidences of chronic diseases. In addition, increasing support from the government and technological innovations in the field of rehabilitation equipment which supports the geriatric population and the physically challenged people is also giving an impetus to this market. As previously stated, the high cost of the rehabilitation equipment, rehabilitation therapies along with a high maintenance cost of such devices alongside an increasing cost of general healthcare services (at least in the US) makes it an enduring problem.*1

According to Persistence Market Research, the global rehabilitation equipment market is forecasted to reach a figure of about US$ 13.4 Billion in 2022 and is poised to exhibit a robust CAGR in the period of assessment.

<img src="https://hackster.imgix.net/uploads/attachments/954151/uploads2ftmp2fe946da20-2267-4c3f-890b-058944f935282fimage_h9T5KbULDJ.png?auto=compress%2Cformat&w=740&h=555&fit=max">

Reiterating on the cost of the therapies and the devices alongside the reduced number or lack of specialists (in relation to the number of patients) there is quite a market for these kind of solutions. Another problem that has to be taken into consideration, is the fact that nowadays and going forward payment will be linked to patient satisfaction and greately related to outcomes. So, patient experience is much more important as a whole. For this project I had the opportunity of actually performing the demonstration to medical specialists and rehabilitation professionals. They immediately found the proposition valuable and at the same time proposed a niche market for the product which is to target it to children. Children are sometimes very difficult to work with, but something such as a Robotic arm has the potential to improve on their attention and adherence to the routine and furthermore on their outcome.

## Regarding SDG's

<img src="https://hackster.imgix.net/uploads/attachments/954172/uploads2ftmp2fddd15ad9-06ec-4e0c-8cd6-58240f1dd3772fimage_XTVQ6lZIAe.png?auto=compress%2Cformat&w=740&h=555&fit=max">

Healthcare is changing, and it has to. Alone the US is reaching almost 20% on its GDP which is unsustainable and the trend that relates payment to patient satisfaction and outcomes will be much more prevalent. Our solution in this case is a combination of two SDGs, the #3 SDG which is to ensure good health and well being for all ages and the #9 which includes to foster innovation. Let's be fair here, even if we advance on health and well being to the limit proposed by the SDG, noncommunicable diseases will always be part of modern life and a sometimes forgoten sector involves orthopaedical-related injuries and rehabilitation. They are both what fills hospitals, and will continue to be for the forseeable future. This solution offers to foster innovation while closing the gap between patient satisfaction and adherence to a treatment for a better outcome. There is seldom a solution like this one for patient satisfaction, and yes a hospital and/or clinic is nowadays filled with technology, but more so related only to critical-care devices and top of the line imaging equipment. This solution focuses much more on the patient as a whole.

## Future Rollout

For the future we wouyld like to actually have a test run in a rehabilitation clinic, but for that we would require some additional funding as we have the capabilities and the networking necessary to accomplish this. The only upgrades perhaps that we would need is everything that goes into contact with the patient as most of our prototype is a one-off and custom-made with the materials we had at hand. The last thing I would like to intergrate in the project is audio cues. This could be done with any STT platform such as Cortana or even Amazon Alexa so that the patient is receiving instructions during the therapy.

Thank you for reading, and I hope you liked the project.


# References:

- https://www.persistencemarketresearch.com/market-research/rehabilitation-equipment-market.asp
- https://www.physio-pedia.com/Rehabilitation_Global_Needs#:~:text=According%20to%20the%202019%20Global,that%20would%20benefit%20from%20rehabilitation.
- https://sensiml.com/documentation/firmware/quicklogic-quickfeather/quicklogic-quickfeather.html
- https://www.healthline.com/health/cool-sculpting-cost
- https://www.hocoma.com/solutions/armeo-power/ https://www.researchgate.net/figure/Examples-of-robotic-devices-for-motor-training-A-End-effector-type-InMotion-20_fig1_259609214
- https://mosquitto.org/


# Table of contents

- [AzureRehab](#azurerehab)
- [Introduction:](#introduction)
- [Materials:](#materials)
- [Connection Diagram:](#connection-diagram)
- [SensiML:](#sensiml)
  - [Sample Examples:](#sample-examples)
  - [Sampling:](#sampling)
  - [Training:](#training)
  - [Model Test: Real Time Labeling:](#model-test-real-time-labeling)
- [Azure TensorFlow Serverless Function:](#azure-tensorflow-serverless-function)
- [WebPage DEMO:](#webpage-demo)
- [Azure VM, MQTT Server:](#azure-vm-mqtt-server)
- [Main UI:](#main-ui)
- [Prototypes:](#prototypes)
  - [FPGA Device:](#fpga-device)
    - [Final:](#final)
  - [Robot Arm:](#robot-arm)
    - [Final:](#final-1)
  - [Full Solution:](#full-solution)
- [Our DEMO:](#our-demo)
- [Business Opportunity](#business-opportunity)
  - [Regarding SDG's](#regarding-sdgs)
  - [Future Rollout](#future-rollout)
- [References:](#references)
- [Table of contents](#table-of-contents)
