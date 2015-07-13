import os
import jpype

import numpy as np

def process_events(reader):

    result = np.zeros((6,6,6,112))

    while reader.hasEvent():
        evt = reader.getNextEvent()
        if evt.hasBank('HitBasedTrkg::HBHits'):
            dchits = evt.getBank('HitBasedTrkg::HBHits')

            hit_data = np.array([
                list(dchits.getInt('sector')),
                list(dchits.getInt('superlayer')),
                list(dchits.getInt('layer')),
                list(dchits.getInt('wire'))]) - 1
            for wire_id in zip(*hit_data):
                result[wire_id] += 1

    return result



if __name__ == '__main__':

    jvm_path = jpype.getDefaultJVMPath()
    curdir = os.path.dirname(os.path.realpath(__file__))
    jars = [os.path.join(curdir,'coat-libs-1.0-SNAPSHOT.jar')]

    def classpath(jars):
        for j in jars:
            if not os.path.isabs(j):
                j = os.curdir+os.sep+j
        return os.pathsep.join(jars)

    try:

        jpype.startJVM(jvm_path, '-Djava.class.path='+classpath(jars))
        java = jpype.JPackage('java')
        java.lang.System.setOut(java.io.PrintStream(java.io.FileOutputStream('/dev/null')))
        java.lang.System.setErr(java.io.PrintStream(java.io.FileOutputStream('/dev/null')))

        EvioFactory = jpype.JClass('org.jlab.evio.clas12.EvioFactory')
        EvioSource = jpype.JClass('org.jlab.evio.clas12.EvioSource')

        EvioFactory.loadDictionary(os.path.join(curdir,'bankdefs'))

        reader = EvioSource()
        reader.dictionary = EvioFactory.getDictionary()
        reader.open('exim1690.0001.recon')
        result = process_events(reader)

    finally:

        jpype.shutdownJVM()


    from matplotlib import pyplot
    from clas12_wiremap import plot_wiremap

    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    pt,(cb,cax) = plot_wiremap(ax,result)
    cax.set_ylabel(r'Hits found in Reconstruction')
    pyplot.show()
