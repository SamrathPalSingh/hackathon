"""
For testing:-

heartRate=167
age=23
sex="Male"
weight=160 pounds
height=75  inches

"""
def bloodPressure(heartRate,age,sex,weight,height):
    weight = weight * 2.2046223302272
    height = height * 0.39370079
    R=18.5
    if sex=="Male":
      Q=5
    else:
      Q=4.5
    ejectionTime=386-(1.64*heartRate)

    bodySurfaceArea=0.007184*(pow(weight,0.425))*(pow(height,0.725))
    strokeVolume=-6.6+(0.25*(ejectionTime-35))-(0.62*heartRate)+(40.4*bodySurfaceArea)-(0.51*age)
    pulsePressure = abs(strokeVolume / ((0.013*weight - 0.007*age-0.004*heartRate)+1.307))
    meanPulsePressure = Q*R

    systolicPressure=(meanPulsePressure + 4.5/3*pulsePressure)
    diastolicPressure=(meanPulsePressure - pulsePressure/3)
    systolicPressure = round(systolicPressure, 2)
    diastolicPressure = round(diastolicPressure, 2)
    print("bp " + str(systolicPressure) + " " + str(diastolicPressure))
    return([systolicPressure, diastolicPressure])
