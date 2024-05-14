# This module facilitates the generation of WIB modules within WIB apps

# Set moo schema search path
from dunedaq.env import get_moo_model_path
import moo.io
moo.io.default_load_path = get_moo_model_path()

# Load configuration types
import moo.otypes

moo.otypes.load_types('wibmod/wibconfigurator.jsonnet')
moo.otypes.load_types('wibmod/protowibconfigurator.jsonnet')

# Import new types
import dunedaq.wibmod.wibconfigurator as wib
import dunedaq.wibmod.protowibconfigurator as protowib


from daqconf.core.app import App, ModuleGraph
from daqconf.core.daqmodule import DAQModule

#===============================================================================
def get_wib_app(nickname, 
                endpoint, 
                version, gain, gain_match, shaping_time, baseline, pulse_dac, pulser, buf, detector_type,
                line_driver,
                wib_pulser_en, wib_pulser_dac, wib_pulser_period, wib_pulser_phase, wib_pulser_duration,
                host="localhost"):
    '''
    Here an entire application consisting only of one (Proto)WIBConfigurator module is generated. 
    '''

    # Define modules

    modules = []

    if version == 1:
       modules += [DAQModule(name = nickname, 
                             plugin = 'ProtoWIBConfigurator',
                             conf = protowib.WIBConf(wib_addr = endpoint,
                                 settings = protowib.WIBSettings(
                                     femb1 = protowib.FEMBSettings(),
                                     femb2 = protowib.FEMBSettings(),
                                     femb3 = protowib.FEMBSettings(),
                                     femb4 = protowib.FEMBSettings()
                                     )
                                 )
                             )]
    else:
        modules += [DAQModule(name = nickname,
                             plugin = 'WIBConfigurator',
                             conf = wib.WIBConf(wib_addr = endpoint,
                                 settings = wib.WIBSettings(
                                     pulser = pulser,
                                     detector_type = detector_type,
                                     femb0 = wib.FEMBSettings(gain=gain, gain_match=gain_match, peak_time=shaping_time, baseline=baseline, pulse_dac=pulse_dac, buffering=buf, test_cap=pulser, line_driver=line_driver),
                                     femb1 = wib.FEMBSettings(gain=gain, gain_match=gain_match, peak_time=shaping_time, baseline=baseline, pulse_dac=pulse_dac, buffering=buf, test_cap=pulser, line_driver=line_driver),
                                     femb2 = wib.FEMBSettings(gain=gain, gain_match=gain_match, peak_time=shaping_time, baseline=baseline, pulse_dac=pulse_dac, buffering=buf, test_cap=pulser, line_driver=line_driver),
                                     femb3 = wib.FEMBSettings(gain=gain, gain_match=gain_match, peak_time=shaping_time, baseline=baseline, pulse_dac=pulse_dac, buffering=buf, test_cap=pulser, line_driver=line_driver),
                                     wib_pulser = wib.WIBPulserSettings(enabled_0=wib_pulser_en, enabled_1=wib_pulser_en, enabled_2=wib_pulser_en, enabled_3=wib_pulser_en, pulse_dac=wib_pulser_dac, pulse_period=wib_pulser_period, pulse_phase=wib_pulser_phase, pulse_duration=wib_pulser_duration)
                                     )
                                 )
                             )]

    mgraph = ModuleGraph(modules)
    wib_app = App(modulegraph=mgraph, host=host, name=nickname)

    return wib_app
