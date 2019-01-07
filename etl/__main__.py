
import io
import sys
from sample import sample_job
from jobrunner import JobRunner
from structure import JobSerializator

def test1():
    job = sample_job()

    jr = JobRunner()
    jr.run(job)

    s = JobSerializator()
    xjob = s.serialize(job)
    print(xjob)
    
    njob = s.deserialize(xjob)
    print(njob.description)
    print(njob.sequence)
    jr.run(njob)

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