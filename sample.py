
from structure import (
    Parameter,
    Field,
    Step,
    Sequence,
    Link,
    Job
)

def sample_job():
    job = Job()
    job.description = "Teste"

    printparameter = Parameter()
    printparameter.name = "text"
    printparameter.type = "str"
    printparameter.value = "Hello World"
    prints = Step()
    prints.type = "Print"
    prints.id = "1234"
    prints.parameters.append(printparameter)
    job.steps.append(prints)

    printparameter2 = Parameter()
    printparameter2.name = "text"
    printparameter2.type = "str"
    printparameter2.value = "Lalalalalalalala"
    prints2 = Step()
    prints2.type = "Print"
    prints2.id = "4567"
    prints2.parameters.append(printparameter2)
    job.steps.append(prints2)

    upperParams1 = Parameter()
    upperParams1.name = "text"
    upperParams1.type = "str"
    upperParams1.value = "aaaaaaaaaaa"
    upperField1 = Field()
    upperField1.name = "result"
    upperField1.type = "str"
    upperField1.variable = "saida1"
    upperStep1 = Step()
    upperStep1.type = "UpperCase"
    upperStep1.id = "5555"
    upperStep1.parameters.append(upperParams1)
    upperStep1.fields.append(upperField1)
    job.steps.append(upperStep1)

    printparameter3 = Parameter()
    printparameter3.name = "text"
    printparameter3.type = "str"
    printparameter3.value = "{{saida1}}"
    print3 = Step()
    print3.type = "Print"
    print3.id = "6666"
    print3.parameters.append(printparameter3)
    job.steps.append(print3)

    inputParams = Parameter()
    inputParams.name = "message"
    inputParams.type = "str"
    inputParams.value = "Insira seu nome: "
    inputField = Field()
    inputField.name = "input"
    inputField.type = "str"
    inputField.variable = "nome"
    inputStep = Step()
    inputStep.type = "UserInput"
    inputStep.id = "7777"
    inputStep.parameters.append(inputParams)
    inputStep.fields.append(inputField)
    job.steps.append(inputStep)

    printparameter4 = Parameter()
    printparameter4.name = "text"
    printparameter4.type = "str"
    printparameter4.value = "O nome inserido foi: {{nome}}"
    print4 = Step()
    print4.type = "Print"
    print4.id = "8888"
    print4.parameters.append(printparameter4)
    job.steps.append(print4)

    seq = Sequence()
    seq.first = "1234"

    link1 = Link()
    link1.idfrom = "1234"
    link1.idto = "4567"
    seq.links.append(link1)

    link2 = Link()
    link2.idfrom = "4567"
    link2.idto = "5555"
    seq.links.append(link2)

    link3 = Link()
    link3.idfrom = "5555"
    link3.idto = "6666"
    seq.links.append(link3)

    link4 = Link()
    link4.idfrom = "6666"
    link4.idto = "7777"
    seq.links.append(link4)

    link5 = Link()
    link5.idfrom = "7777"
    link5.idto = "8888"
    seq.links.append(link5)

    job.sequence = seq

    return job