from py21cmsense import GaussianBeam, Observatory, Observation, PowerSpectrum, hera
import numpy as np

def to_cm_if():
    sensitivity = PowerSpectrum(
        observation = Observation(
            observatory = Observatory(
#                antpos = hera(hex_num=7, separation=14, dl=12.12, units="m"),
                antpos = hera(hex_num=7, separation=14, dl=12.12),
                beam = GaussianBeam(frequency=135.0, dish_size=14),
                latitude=38*np.pi/180.0
            )
        )
    )
    power_std = sensitivity.calculate_sensitivity_1d()
    print("sens=",sensitivity.k1d)
    print("pow=",power_std)
    z=zip(sensitivity.k1d, power_std)
    print("sensitivity.k1d is a ",type(sensitivity.k1d)," and power_std is a ",type(power_std))
    a=[1,2,3]
    b=[4,5,6]
    c=zip(a,b)
    print("a=",a,", b=",b,", c=",c)
    d=dict(c)
    print(d)
    dd=dict(z)
#    print(dd)
#    print dict(zip([v.value for v in sensitivity.k1d], [v.value for v in power_std]))
    z=zip([v.value for v in sensitivity.k1d], [v.value for v in power_std])
    print(dict(z))


def run():
    to_cm_if();

if __name__ == '__main__':
    run()
