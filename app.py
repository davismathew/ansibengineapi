#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
#from pingTest import pingTest
from ansible_utils import get_path
from play_util.AnsiblePlaybook import AnsiblePlaybook
from tools_util.TracePath import tracePath
import os

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'netbot':
        return 'N#tB@t'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#### Sample POST API

#@app.route('/cmapp/api/v1.0/allRowPingTest', methods=['POST'])
#@auth.login_required
#def allRowPingTest():
#    if not request.json or not 'value' in request.json:
#        abort(400)
#    # { ca : cAEnd, cai : cAEndInt, caa:cAEndIP, cz:cZEnd, czi:cZEndInt, cza:cZEndIP}
#    data = str(request.json['value'])
    # print data
#    info = data.split("*")
    # print info
#    cout = len(info) - 1
#    fInfo = []
#    for dt in range(1, cout):
#        val = str(info[dt]).split(',')
#        # print val
#        fInfo.append([val[4], val[5], val[6], val[7], val[8], val[9]])

    # print  "final output :-",fInfo
 #   object = pingTest()
 #   value = object.ping(fInfo)
 #   print value
 #   ret_data = {"value": value}
#    return jsonify(ret_data), 201



routers = [
    {
        'id': 1,
        'routerip': u'10.10.10.102'
    },
    {
        'id': 2,
        'routerip': u'10.10.10.104',
    }
]


def make_routers(task):
    routerlist = {}
    for field in task:
        if field == 'id':
           routerlist['uri'] = url_for('get_routers', task_id=routers['id'], _external=True)
        else:
            routerlist[field] = routers[field]
    return routerlist

#### Sample GET API

#/etc/ansiblestdout/stdout160.out
@app.route('/cmapp/api/v1.0/routers', methods=['GET'])
@auth.login_required
def get_routers():
    return jsonify({'routers': routers})

@app.route('/cmapp/api/v1.0/routerlist', methods=['POST'])
@auth.login_required
def get_postrouters():
    if not request.json or not 'title' in request.json:
        abort(400)
    stdoutfile = '/etc/ansiblestdout/stdout160.out'
        # retdata = {'value':stdoutfile}
        # playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
        # Output=playbook.runPlaybook()
    fileRead=open(stdoutfile)
    Output=fileRead.read()
        # # print Output
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    retdata={'value':Output}
    return jsonify(retdata), 201
  #  temp=''
  #  temp = request.json['title']
  #  return jsonify({'routers': temp}),201

@app.route('/ansibengine/api/v1.0/altinventory', methods=['POST'])
@auth.login_required
def inventory():
    if not request.json or not 'variable' in request.json or not 'inventory' in request.json:
        abort(400)
    variable = request.json['variable']
    inventory = request.json['inventory']
    filepath = '/home/davis/Documents/Network-automation/'
    inventoryfile = filepath+variable
    target = open(inventoryfile, 'w')
    target.write('[routerxe]')
    target.write("\n")
    target.write(inventory)
    retdata={"value":"Success"}
    return jsonify(retdata), 201

@app.route('/ansibengine/api/v1.0/getinterfacetraceroute', methods=['POST'])
@auth.login_required
def getinterfacetraceroute():
    if not request.json or not 'interfaceip' in request.json or not 'destip' in request.json or not 'routerip' in request.json:
        abort(400)
    routerip = request.json['routerip']
    interfaceip = request.json['interfaceip']
    destip = request.json['destip']
    vrf = request.json['vrf']
#    sourceip=request.args.get('source_ip')
#    destip=request.args.get('dest_ip')
#    vrf=''
#    if request.args.get('vrf') is not None:
#        vrf=request.args.get('vrf')
    vrfname=request.json['vrfname']
    target = open('/home/davis/Documents/Network-automation/tracerouteinterfaceinv', 'w')
    target.write('[routerxe]')
    target.write("\n")
    target.write(str(routerip))
    commands=''
    if vrf is True:
        commands='commands: traceroute vrf '+vrfname+' '+str(destip)
    else:
        commands='commands: traceroute '+str(destip)+' source '+str(interfaceip)+' numeric'

    target = open('/home/davis/Documents/Network-automation/tracecommandinterface.yaml', 'w')
    target.write('---')
    target.write("\n")
    target.write(commands)
    retdata={'value':"Success"}
    return jsonify(retdata), 201

@app.route('/ansibengine/api/v1.0/runinterfacetraceroute', methods=['POST'])
@auth.login_required
def runinterfacetraceroute():
#    if not request.json:
#        abort(400)
#    t raceip = str(request.json['ip'])
#    if not request.json or not 'ip' in request.json:
#       abort(400)
#    ip=request.json['ip']

#    traceip=str(request.form['ip'])
    playbookName = 'tracerouteinterface.yml'
    inventory = 'tracerouteinterfaceinv'
    stdoutfile = '/etc/ansiblestdout/interfacetraceroute.out'
#        target = open('/home/davis/Documents/Network-automation/tracecommand.yaml', 'w')
#        target.write('---')
#        target.write("\n")
#        target.write('commands: traceroute '+traceip)

        # retdata = {'value':stdoutfile}
        # target = open('/home/davis/Documents/Network-automation/tracerouteinv', 'w')
        # target.write('[routerxe]')
        # target.write("\n")
        # target.write('10.10.10.102')

    playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
    Output=playbook.runPlaybook()
    fileRead=open(stdoutfile)
    Output=fileRead.read()
    # print Output
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    flag=False
    factname = open('/etc/netbot/factshare.txt','r')
    factpath = factname.read()
    if not factpath:
        flag=True
    factfullname = "/etc/ansiblefacts/"+factpath

#        match=re.match(r'.*\s+failed\=[1-9]+\s+.*',str(Output),re.DOTALL)
    if flag:
        outvar="playbook not run. \n"
        retdata={'value':outvar}
        return jsonify(retdata)
    else:
#               factname = open('/etc/netbot/factshare.txt','r')
#               factpath = factname.read()
#               factfullname = "/etc/ansiblefacts/"+factpath


        tPath=tracePath('ops.emc-corp.net','svcorionnet@emc-corp.net','$V(0r!0N3t')
        rPath=tPath.getPath(factfullname)
        outvar=''
        if isinstance(rPath, list):
                for path in rPath:
                        outvar=outvar+path
                        outvar=outvar+"\n"
        else:
                outvar=rPath
        # fileRead=open(stdoutfile)
        # Output=fileRead.read()
        # # print Output
        #Output=Output.replace("[0;32m","")
        #Output=Output.replace("[0;31m","")
        #Output=Output.replace("[0m"," ")
        #Output=Output.replace("\x1b"," ")
        retdata={'value':outvar}
        return jsonify(retdata)

    ret_data={'value':"an error has occured"}
    return jsonify(ret_data)

@app.route('/ansibengine/api/v1.0/gettraceroute', methods=['POST'])
@auth.login_required
def gettraceroute():
    if not request.json or not 'sourceip' in request.json or not 'destip' in request.json:
        abort(400)
    sourceip = request.json['sourceip']
    destip = request.json['destip']
    vrf = request.json['vrf']
#    sourceip=request.args.get('source_ip')
#    destip=request.args.get('dest_ip')
#    vrf=''
#    if request.args.get('vrf') is not None:
#        vrf=request.args.get('vrf')
    vrfname=request.json['vrfname']
    target = open('/home/davis/Documents/Network-automation/tracerouteinv', 'w')
    target.write('[routerxe]')
    target.write("\n")
    target.write(str(sourceip))
    commands=''
    if vrf is True:
        commands='commands: traceroute vrf '+vrfname+' '+str(destip)
    else:
        commands='commands: traceroute '+str(destip)

    target = open('/home/davis/Documents/Network-automation/tracecommand.yaml', 'w')
    target.write('---')
    target.write("\n")
    target.write(commands)
    retdata={'value':"Success"}
    return jsonify(retdata), 201
#    return render_template('ansible/traceroute.html', ip=destip)

@app.route('/ansibengine/api/v1.0/runtraceroute', methods=['POST'])
@auth.login_required
def runtraceroute():
#    if not request.json:
#        abort(400)
#    t raceip = str(request.json['ip'])
#    if not request.json or not 'ip' in request.json:
#    	abort(400)
#    ip=request.json['ip']

#    traceip=str(request.form['ip'])
    playbookName = 'tracerouteip.yml'
    inventory = 'tracerouteinv'
    stdoutfile = '/etc/ansiblestdout/traceroute.out'
#        target = open('/home/davis/Documents/Network-automation/tracecommand.yaml', 'w')
#        target.write('---')
#        target.write("\n")
#        target.write('commands: traceroute '+traceip)

        # retdata = {'value':stdoutfile}
        # target = open('/home/davis/Documents/Network-automation/tracerouteinv', 'w')
        # target.write('[routerxe]')
        # target.write("\n")
        # target.write('10.10.10.102')

    playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
    Output=playbook.runPlaybook()
    fileRead=open(stdoutfile)
    Output=fileRead.read()
    # print Output
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    flag=False
    factname = open('/etc/netbot/factshare.txt','r')
    factpath = factname.read()
    if not factpath:
    	flag=True
    factfullname = "/etc/ansiblefacts/"+factpath

#        match=re.match(r'.*\s+failed\=[1-9]+\s+.*',str(Output),re.DOTALL)
    if flag:
    	outvar="playbook not run. \n"
    	retdata={'value':outvar}
    	return jsonify(retdata)
    else:
#               factname = open('/etc/netbot/factshare.txt','r')
#               factpath = factname.read()
#               factfullname = "/etc/ansiblefacts/"+factpath


    	tPath=tracePath('ops.emc-corp.net','svcorionnet@emc-corp.net','$V(0r!0N3t')
    	rPath=tPath.getPath(factfullname)
    	outvar=''
    	if isinstance(rPath, list):
    		for path in rPath:
    			outvar=outvar+path
    			outvar=outvar+"\n"
    	else:
      		outvar=rPath
        # fileRead=open(stdoutfile)
        # Output=fileRead.read()
        # # print Output
        #Output=Output.replace("[0;32m","")
        #Output=Output.replace("[0;31m","")
        #Output=Output.replace("[0m"," ")
        #Output=Output.replace("\x1b"," ")
     	retdata={'value':outvar}
     	return jsonify(retdata)

    ret_data={'value':"an error has occured"}
    return jsonify(ret_data)


@app.route('/ansibengine/api/v1.0/resultout', methods=['POST'])
@auth.login_required
def get_resultout():
    if not request.json or not 'resultid' in request.json:
        abort(400)
    resultid = request.json['resultid']
    stdoutfile = '/etc/ansiblestdout/stdout160.out'
        # retdata = {'value':stdoutfile}
        # playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
        # Output=playbook.runPlaybook()
    fileRead=open(stdoutfile)
    Output=fileRead.read()
        # # print Output
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    retdata={'value':Output}
    return jsonify(retdata), 201
  #  temp=''
  #  temp = request.json['title']
  #  return jsonify({'routers': temp}),201

@app.route('/ansibengine/api/v1.0/playbooklist', methods=['GET'])
def playbooklist():
#    if not request.json or not 'resultid' in request.json:
#        abort(400)
#    resultid = request.json['resultid']
#    stdoutfile = '/etc/ansiblestdout/stdout160.out'
        # retdata = {'value':stdoutfile}
        # playbook=AnsiblePlaybook(playbookName,inventory,stdoutfile)
        # Output=playbook.runPlaybook()
 #   fileRead=open(stdoutfile)
 #   Output=fileRead.read()
        # # print Output
 #   Output=Output.replace("[0;32m","")
 #   Output=Output.replace("[0;31m","")
 #   Output=Output.replace("[0m"," ")
 #   Output=Output.replace("\x1b"," ")
    files=[]
    temp=os.listdir("/home/davis/Documents/Network-automation")
    for file in temp:
        if file.endswith(".yml"):
            files.append(file)
    temp=['new','another']
    retdata={'value':files}
    return jsonify(retdata), 201
  #  temp=''
  #  temp = request.json['title']
  #  return jsonify({'routers': temp}),201

@app.route('/ansibengine/api/v1.0/sharefact', methods=['POST'])
@auth.login_required
def sharefact():
    if not request.json or not 'fact' in request.json:
        abort(400)
    fact = request.json['fact']
    if fact != "nofile":
        target = open('/home/davis/Documents/Network-automation/sharedvalues.yaml', 'w')
        target.write('---')
        target.write("\n")
        target.write('guivars: /etc/ansiblefacts/'+str(fact))
    Output="Success"
    retdata={'value':Output}
    return jsonify(retdata), 201

@app.route('/ansibengine/api/v1.0/runplaybook', methods=['POST'])
@auth.login_required
def runplaybook():
    if not request.json or not 'playbook' in request.json or not 'inventory' in request.json or not 'resultid' in request.json:
        abort(400)
    
    playbook = request.json['playbook']
    inventory = request.json['inventory']
    resultid = request.json['resultid']
#    fact = request.json['fact']
    stdoutfilename = "stdout"+resultid+".out"
    stdoutpath = get_path('resultout')
    stdoutfile = stdoutpath+"/"+stdoutfilename
    playbookName = playbook
    inventory = inventory
#    if fact != "nofile":
#    	target = open('/home/davis/Documents/Network-automation/sharedvalues.yaml', 'w')
#    	target.write('---')
#    	target.write("\n")
#    	target.write('guivars: /etc/ansiblefacts/'+str(fact))
    print "initial"
#    editresult.outfile = stdoutfile
    # retdata = {'value':stdoutfile}
    playbookinst=AnsiblePlaybook(playbookName,inventory,stdoutfile)
    Output=playbookinst.runPlaybook()
    fileRead=open(stdoutfile)
    Output=fileRead.read()
    # print Output
    print "test"
    Output=Output.replace("[0;32m","")
    Output=Output.replace("[0;31m","")
    Output=Output.replace("[0m"," ")
    Output=Output.replace("\x1b"," ")
    retdata={'value':Output}
    return jsonify(retdata), 201

if __name__ == '__main__':
    app.run(host='200.12.221.13',port=5555,debug=True)
