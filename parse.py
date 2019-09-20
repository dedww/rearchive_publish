from __future__ import print_function 
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
import sqlite3
import json
import transaction
import path_system

SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly' #set premission
conn = sqlite3.connect('db') #connect to DB
c = conn.cursor()

#JSON create procedure
def json_create(c_folders): 
    print('cf ',c_folders)
    array = list()
    edgearray = list()

    for i in range(c_folders):
        if i == 0:
            node = {'id': 'root', 'name': 'root', 'href': ''}
            data = {'data': node}
            array.append(data)
        else:

            c.execute('''SELECT id FROM nodes WHERE rowid = ''' + str(i))
            data_id = c.fetchall()
            print('data_id',str(data_id).strip("[](),'"))
            c.execute('''SELECT name FROM nodes WHERE rowid = ''' + str(i))
            data_name = c.fetchall()
            c.execute('''SELECT href FROM nodes WHERE rowid = ''' + str(i))
            data_href = c.fetchall()

            node = {'id': str(data_id).strip("[](),'"), 'name': str(data_name).strip("[](),'"),'href': str(data_href).strip("[](),'")}
            data = {'data': node}
            array.append(data)

        if i > 0:
            c.execute('''SELECT source_data FROM edges WHERE rowid = ''' + str(i))
            data_source = c.fetchall()
            c.execute('''SELECT target_data FROM edges WHERE rowid = ''' + str(i))
            data_target = c.fetchall()

            edge = {'source': str(data_source).strip("[](),'"), 'target': str(data_target).strip("[](),'")}
            data = {'data': edge}
            edgearray.append(data)

    final = {'nodes': array, 'edges': edgearray}
    with open('static/folders.json', 'w') as outfile:
        json.dump(final, outfile)

#parsing foders tree
def parse(service):
    c.execute('''DROP TABLE IF EXISTS nodes''')
    c.execute('''DROP TABLE IF EXISTS edges''')
    c.execute('''CREATE TABLE IF NOT EXISTS nodes
                (id text, name text, href text
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS edges
                (source_data text, target_data text
                );''')
    temp_list = ['root']
    i = 0
    c_folders = 0
    while i < len(temp_list):
        temp_root_folder = temp_list[i]
        results = service.files().list(
            pageSize=20,
            q='"' + temp_root_folder + '"' + ' in parents and mimeType = "application/vnd.google-apps.folder"',
            fields='nextPageToken,files(id, name)').execute()
        items = results.get('files', [])
        for item in items:
            if item['id'] != '':
                temp_list.append(item['id'])
                node = [(item['id'], item['name'], 'https://drive.google.com/drive/folders/' + item['id'])]
                print(node)
                edge = [(temp_root_folder, item['id'])]
                print(edge)
                c.executemany("INSERT INTO nodes VALUES(?,?,?)", node)
                conn.commit()
                c.executemany("INSERT INTO edges VALUES(?,?)", edge)
                conn.commit()
                c_folders =+ 1
        i = i + 1
        print(i)
    return (i)

def main():
    store = oauth_file.Storage(path_system.path() + 'token.json') #set Google administration file
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(path_system.path() + 'credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    c_folders = parse(service) 
    json_create(c_folders)

if __name__ == "__main__":
    main()
