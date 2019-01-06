import xxml
import re

from steps import execution_steps_definition

class JobRunner:
    re_values = re.compile(r"\{\{(\w+)\}\}")

    def run(self, job):
        drun = dict([(s.id, s) for s in job.steps])
        first = job.sequence.first
        variables = {}
        self._run_step(job, first, drun, variables)

    def _run_step(self, job, sid, drun, variables):
        if sid in drun:
            step = drun[sid]
            if step.type in execution_steps_definition:
                es = execution_steps_definition[step.type]()
                for p in step.parameters:
                    setattr(es, p.name, self._parse_values(p.value, variables))
                es.execute()

                for field in step.fields:
                    variables[field.variable] = getattr(es, field.name)

            links = [link for link in job.sequence.links if link.idfrom == sid]
            for link in links:
                self._run_step(job, link.idto, drun, variables.copy())

    def _parse_values(self, valuesstr, variables):
        value = valuesstr
        for key in JobRunner.re_values.findall(valuesstr):
            value = value.replace("{{" + key + "}}", variables.get(key, ""))
        return value