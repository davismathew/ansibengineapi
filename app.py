#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
#from pingTest import pingTest
from ansible_utils import get_path
from play_util.AnsiblePlaybook import AnsiblePlaybook
from tools_util.TracePath import tracePath

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


@app.route('/ansibengine/api/v1.0/runplaybook', methods=['POST'])
@auth.login_required
def runplaybook():
    if not request.json or not 'playbook' in request.json or not 'inventory' in request.json or not 'resultid' in request.json:
        abort(400)
    
    playbook = request.json['playbook']
    inventory = request.json['inventory']
    resultid = request.json['resultid']
    stdoutfilename = "stdout"+resultid+".out"
    stdoutpath = get_path('resultout')
    stdoutfile = stdoutpath+"/"+stdoutfilename
    playbookName = playbook
    inventory = inventory
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
