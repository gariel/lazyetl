
import io
import sys
from jobrunner import JobRunner
from structure import JobSerializator

def main(filename="examples/simple.xml"):
    with io.open(filename) as f:
        xmltext = f.read()

    s = JobSerializator()
    job = s.deserialize(xmltext)

    jr = JobRunner()
    jr.run(job)

if __name__ == '__main__':
    args = sys.argv
    #test1()
    if len(args) > 1:
        main(args[1])
    else:
        main()