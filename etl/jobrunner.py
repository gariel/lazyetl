import xxml
import re

from steps import definition

class JobRunner:
    re_values = re.compile(r"\{\{(\w+)\}\}")

    def run(self, job):
        drun = {s.id: s for s in job.steps}
        first = job.sequence.first
        variables = {}
        self._run_step(job, first, drun, variables)

    def _run_step(self, job, sid, drun, variables):
        step = drun[sid]
        if step.type not in definition:
            raise Exception("Step definition '{}' not found".format(step.type))

        es = definition[step.type]()
        for p in step.parameters:
            setattr(es, p.name, self._parse_values(p.type, p.value, variables))

        es.execute()

        def next_steps():
            links = [link for link in job.sequence.links if link.idfrom == sid]
            for link in links:
                self._run_step(job, link.idto, drun, variables)

        if step.fields:
            variables = variables.copy()
            results = {field.name: getattr(es, field.name) for field in steps.fields}
            # {"Xml": <>, "steps": [], "links": []}
            variables.update(results)
            next_steps()
        else:
            next_steps()

    def _parse_values(self, partype, valuekey, variables):
        if partype == "str":
            value = valuekey
            for key in JobRunner.re_values.findall(valuekey):
                value = value.replace("{{" + key + "}}", variables.get(key, ""))
            return value
        else:
            return variables.get(valuekey, None)