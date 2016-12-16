
from math import isnan
from math import pi
from math import sqrt
from math import log
from math import sin

class Cannon(object):
    GUN_POWDER_DENSITY = 881.071383
    CAST_IRON_DENSITY = 6800
    R = 56496.1 # Metric Ratio
    ATM = 2872.310354

    def __init__(self, boreWidth, boreLength, launchAngle, platformHeight, gunPowderMass):
        self.boreWidth = boreWidth
        self.boreLength = boreLength
        self.launchAngle = launchAngle
        self.platformHeight = platformHeight
        self.gunPowderMass = gunPowderMass

    @property
    def chargeLength(self):
        den = (pi * self.boreWidth * self.boreWidth * self.GUN_POWDER_DENSITY)
        if den == 0:
            return 0
        else:
            return self.gunPowderMass * 4 / den

    @property
    def muzzleVelocity(self):
        muzzleVelocity = 0

        if (self.chargeLength + self.boreWidth > self.boreLength):
            muzzleVelocity = 0
        else:
            if ((self.ballMass + self.gunPowderMass / 3) == 0) | (self.chargeLength == 0):
                muzzleVelocity = 0
            else:
                muzzleVelocity = (
                        sqrt(2 * self.R * self.ATM / self.GUN_POWDER_DENSITY) *
                        sqrt(self.gunPowderMass / (self.ballMass + self.gunPowderMass / 3) *
                            log(self.boreLength / self.chargeLength)
                        )
            )
            if isnan(muzzleVelocity):
                muzzleVelocity = 0

        return muzzleVelocity

    @property
    def ballMass(self):
        return (4/3) * pi * self.CAST_IRON_DENSITY * pow((self.boreWidth / 2), 3)


    @property
    def startHeight(self):
        angleRadians = self.launchAngle * pi / 180
        cannonToPlatformHeight = sin(angleRadians) * self.boreLength
        return cannonToPlatformHeight + self.platformHeight

#boreWidth, boreLength, launchAngle, platformHeight, gunPowderMass
def main():
    cannon = Cannon(0.09271, 1.48336, 45, 0, 0.5669905 )
    print(str(cannon.chargeLength))
    print(str(cannon.muzzleVelocity))
    print(str(cannon.ballMass))
    print(str(cannon.startHeight))

if __name__ == "__main__":
    # execute only if run as a script
    main()
