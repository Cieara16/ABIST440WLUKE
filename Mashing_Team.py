#Brian Tu's Section

class Mashing(object):
    def __init__(self, ratio, tempoftarget, weightofgrain, tempofgrain, timeofboil, sizeofbatch, lossoftrub, lossoftun):
        self.ratio = ratio
        self.tempoftarget = tempoftarget
        self.weightofgrain = weightofgrain
        self.tempofgrain = tempofgrain
        self.timeofboil = timeofboil
        self.sizeofbatch = sizeofbatch
        self.lossoftrub = lossoftrub
        self.lossoftun = lossoftun


def strikeTemp(self):
    # This is calculating the strike water temperature#
    return round(
        ((.2 / (float(self.ratio)) * (float(self.tempoftarget) - float(self.tempofgrain)) + float(self.tempoftarget))),
        2)


def strikeVol(self):
    # This is calculating the water volume#
    return round(((self.ratio * self.weightofgrain) / 4), 2)

#Eni Saraci Section

def volofsparge(self):
    # This procedure calculates the volume of water that is needed in order to start sparging phase#
    return self.totalofwater() - self.volstrike()


def totalofwater(self):
    # This procedure calculates the amount of water needed for the brewing procedure along with the losses during this phase#
    return round((self._preboilvol() + self.lossoftun + self._absorption()), 2)


def absorption(self):
    # This procedure calculates the amount of water lost during absorption process#
    return (self.weightofgrain * .15)

#YongKang Deng Section

def lossofmashtun(self):
    # Procedure used to calculate the amount of water that was lost in the mash tun due to transferring to the boil kettle#
    return (((self.volofstrike() - (self._absorption()) - self.lossoftun)))


def rateofevap(self):
    # Procedure to calculate the amount of water that was lost to evaporation in the boil phase#
    rateofevap = .10  # The rate of evaporation per hour
    return round(1 - (rateofevap * (self.timeofboil / 60)), 2)


def lossofshrink(self):
    # Procedure to calculate the amount of water lost due to cooling of the wort.
    # 4 percent is the standard shrink factor.
    return 1 - .04


def volofpreboil(self):
    # Procedure to calculate the amount of water needed during pre boil#
    return round((((self.sizeofbatch + self.lossoftrub) / self._lossofshrink()) / self._rateofevap()), 2)

#Nicolas Galindo Section

if __name__ == "__main__":
	sizeofbatch = 5    #Gallons
	ratio = 1.25     #Quarts
	tempofmash = 152   #Fahrenheit
	weightofgrain = 11 #Pounds
	tempofgrain = 70   #Fahrenheit
	timeofboil = 60    #Minutes
	#This process depends on the system
	#Gallons:
	lossoftrub= 0
	lossoftun= 0

	mash = Mashing(weightofgrain, timeofboil, tempofmash, ratio, sizeofbatch, lossoftrub, tempofgrain, lossoftun)
#{0} Fahrenheit - Temperature of Strike Water#
	print(mash.strikeTemp())

#{0} Gallons - Volume of Strike Water#
	print(mash.strikeVol())

#{0} Gallons - Volume of Sparge Water#
	print(mash.spargeVol())

#{0} Gallons - Amount of Water Needed#
	print(mash.totalWaterNeeded())

#{0} Gallons - Mash process absorbed by grain#
	print(mash._absorption())

#{0} Gallons - First outcomes #
	print(mash._mashlossoftun())

#{0} Gallons -Amount during Pre Boil #
	print(mash._preboilamount())

#{0} Gallons - Amount lost after evaporation during {1} minute boil#
	print(mash._preboillamount()-(mash._preboilamount()*mash._rateofevap()),mash.timeofboil)

#{0} Gallons -Amount that was lost to shrinking after reducing wort temperature.#
	print(mash._preboilamount()*mash._rateofevap()-5)