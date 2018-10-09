import urllib2
# from PIL import Image
import pyDes
# import PIL.Image
# import base64
import hashlib
from flask import Flask, render_template, request

# from Crypto.Cipher import AES
import swiftclient
import keystoneclient
import os

# from simple_aes_cipher import cipher
f1 = ''
totalsize = ''
size = ''
auth_url = 'https://identity.open.softlayer.com' + '/v3'
projectId = '92e6d2e713fb45cd9dda22d53f963fa8'
region = 'dallas'
userId = 'f37a115fd99d49b6b0617851a89a38be'
password = 'yg~AGMGvLN&TY25M'
container_name = 'vir', 'Virti'
conn = swiftclient.Connection(key=password,
                              authurl=auth_url,
                              auth_version='3',
                              os_options={"project_id": projectId,
                                          "user_id": userId,
                                          "region_name": region})
# dpath = 'C:/Users/Virti Sanghavi/Downloads/get-started-python-master/download'
dpath = ''
folder = 'C:/Users/Virti Sanghavi/Downloads/get-started-python-master/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'jpg', 'jpeg', 'gif', 'xml'])

k = pyDes.des("DESCRYPT", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = folder

dic = {}


@app.route('/', methods=['POST', 'GET'])
def main_page():
    res = ""
    file_download = ""
    if request.method == 'POST':
        if request.form['submit'] == 'Upload':
            global f1
            f1 = request.files['file_upload']
            key = request.form['key']
            # print 'a'
            upload(f1.filename)

        elif request.form['submit'] == 'Download':
            f1 = request.form['file_download']
            dkey = request.form['dkey']
            # print f1
            download(f1)


        elif request.form['submit'] == 'List':
            # print 'list'
            res = list()


        elif request.form['submit'] == 'Remove':
            size = request.form['fsize']
            remove(size)

    return render_template('index1.html', res=res)


def upload(filename):
    # fname, ext = os.path.splitext(filename)
    # if ext == ".txt":
    global f1
    fl = request.files['file_upload']
    filename = str(f1.filename)
    data = fl.read()
    #  content=encrypt_val(data,key)
    # print 'data'+ data
    # contents = cipher.encrypt(data,ukey)
    no = checksum(data)
    # print'hi'+ no
    text = data + '$$$$$$$$$' + no
    # contents = k.encrypt(text)
    contents = text
    dic[f1.filename] = no
    # print 'hello'+ dic[f1.filename]
    # print contents
    fname, ext = os.path.splitext(f1.filename)
    # print fname
    # if ext == ".txt":
    global size
    if size <= '10000':

        conn.put_object('vir', f1.filename, contents, content_type='text/plain')
    else:
        # imagefile = Image.open('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files' + "/" + filename)
        # contents = open('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files' + "/" + filename, 'rb').read()
        # contents = base64.b64encode('C:/Users/srinivas venkatesh/Documents/cloud computing/assg1/files/' + filename)
        # This has to be reviewed and removed
        conn.put_object('Virti', f1.filename, contents, content_type='text/plain')
    # print filename
    fl.close()


def checksum(data):
    global f1
    md5 = hashlib.md5()
    md5.update(data)
    # print 'function' + md5.hexdigest()
    return md5.hexdigest()
    # do something


def list():
    # print ("nObject List:")
    list = ""
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            # print container['name']

            # print "object: {0} size: {1} date: {2}'.format(data['name'], data['bytes'], data['last_modified'])"
            list += (
            '\r\nobject: {0} size: {1} date: {2}\r\n'.format(data['name'], data['bytes'], data['last_modified']))
            # list += ('\r\nobject: {0} size: \r\n'.format(data['bytes']))
            #  global totalsize
            # totalsize = data['bytes']
            # totalsize+=data['bytes']
            # print '<h3>Total size in bytes is</h3>';
            # return totalsize


            # totalsize+=size
            # list+=('\r\n totalsize: {0} size:')
            # @app.route('/upload')
            # def upload():
            #  return render_template('upload.html')

            #    totalsize = 0
            #    filesize = os.path.getsize(filename)
            #    filesize = filesize / 2048
            #
            # for container in conn.get_account()[1]:
            #         for data in conn.get_container(container['name'])[1]:
            #
            #            totalsize = totalsize + data['bytes']
            #            totalsize = totalsize / 2048
            #            filesizeafter = filesize + totalsize
            #            return filesizeafter

    return list


def download(filename):
    # print filename
    fname, ext = os.path.splitext(filename)
    # for files in conn.get_container(container_name)[1]:
    # if filename == files['name']:
    # print "Fname  ",fname,"  extn  ",ext
    for container in conn.get_account()[1]:
        # print "Container ",container
        for data1 in conn.get_container(container['name'])[1]:
            # print filename
            # print data1['name']
            if filename == data1['name']:
                # print "in if"
                try:
                    fobj = conn.get_object(container['name'], filename)
                    # print fobj
                    # contents = k.decrypt(dfile)
                    # print 'a'
                    # if ext == '.txt':
                    # open()
                    with open(filename, 'wb') as fw:
                        data = str(fobj)
                        fw.write(data)
                        fw.close()


                except urllib2.HTTPError as err:
                    if err.code == 404:
                        continue
                # print 'Filename download is'
                # print filename
                return render_template('index1.html', file_download=filename)


def remove(size):
    for container in conn.get_account()[1]:
        for data in conn.get_container(container['name'])[1]:
            print data['bytes']
            if int(data['bytes']) < int(size):
                conn.delete_object(container['name'], data['name'])


port = int(os.getenv('VCAP_APP_PORT', 8080))
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    # For Local Runn
    # For Local Runn
    # app.run(debug=True,host = '0.0.0.0', port=port)

