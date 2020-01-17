# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 21:29:01 2020

@author: eckar
"""

import os
import json
import dateutil.parser as dp


importFile=r'C:\Users\eckar\org2\Wunderlist-20200111\Tasks.json'
wunderlistImportName='Wunderlist Import'
targetDir=r'C:\Users\eckar\org10'



def bufferToFile(buffer,id):
    
    
    filename = targetDir+os.path.sep+'%032x'%id+'.md'
    f=open(filename,"w",encoding='utf-8',errors='ignore',newline='\n')
    isNextLine=False
    
    for b in buffer:
        if isNextLine:
            f.write('\n')    
        try:
            f.write(b) 
        except UnicodeEncodeError as e:
            print(e)
            print (f'at file {filename}')
            f.write(b.encode('latin-1'))
        isNextLine=True
    f.close()
    

globalId=0

class GlobalId:
    
    def nextGlobalId():
        global globalId
        
        globalId=globalId+1
        return globalId


def getNullCheckValue(jsonData,attribute):
    if (not isinstance(jsonData[attribute],str)) or jsonData[attribute]=='null':
        return '0'
    else:
        return jsonData[attribute]


def getNullCheckTimeInMillis(jsonData,attribute):
    if (not isinstance(jsonData[attribute],str)) or jsonData[attribute]=='null':
        return '0'
    else:
        return '%i'%dp.isoparse(jsonData[attribute]).timestamp()



class Task:
    def __init__(self,jsonData,parent):
        self.jsonData=jsonData
        self.id=GlobalId.nextGlobalId()
        self.parent=parent
        
    def createContent(self):
        buffer = []
        
        buffer.append(self.jsonData['title'])
        buffer.append("")
        
        for c in self.jsonData['notes']:
            if c!=None:
                buffer.append(c['content'])
        buffer.append("")
        buffer.append('id: '+'%032x'%self.id)
        buffer.append('parent_id: '+'%032x'%self.parent.id)
        buffer.append("created_time: "+self.jsonData['createdAt'])
        
        buffer.append("updated_time: 0")
        buffer.append("is_conflict: 0")
        buffer.append("latitude: 0.00000000")
        buffer.append("longitude: 0.00000000")
        buffer.append("altitude: 0.0000")
        
        buffer.append("author: "+(self.jsonData['createdBy'])['email'])
        buffer.append("source_url: ")

        buffer.append("is_todo: 1")
        buffer.append("todo_due: "+getNullCheckTimeInMillis(self.jsonData,'dueDate'))
        buffer.append("todo_completed: "+getNullCheckTimeInMillis(self.jsonData,'completedAt'))
        buffer.append("source: Wunderlist")
        buffer.append("source_application: WunderlistToJoplin")
        buffer.append("application_data: ")
        buffer.append("order: 0")
        buffer.append("user_created_time: "+getNullCheckValue(self.jsonData,'createdAt'))
        buffer.append("user_updated_time: "+getNullCheckValue(self.jsonData,'createdAt'))
        buffer.append("encryption_applied: 0")
        buffer.append("markup_language: 1")
        buffer.append("type_: 1")
        
        bufferToFile(buffer,self.id)
        
        
class List:
    def __init__(self,jsonData):

        self.jsonData=jsonData
        self.id=GlobalId.nextGlobalId()
                
        self.folder=Folder.getFolder(self.jsonData['folder'],self)
        
        self.tasks=[]
        for task in self.jsonData['tasks']:
            self.tasks.append(Task(task,self))    
        
        
        
    def createContent(self):
        
        for task in self.tasks:
            task.createContent()
        
        buffer = []
        
        buffer.append(self.jsonData['title'])
        buffer.append("")
        buffer.append('id: '+'%032x'%self.id)
        buffer.append("created_time: "+self.jsonData['createdAt'])
        buffer.append("updated_time: 0")
        buffer.append("user_created_time: "+self.jsonData['createdAt'])
        buffer.append("user_updated_time: 0")
        buffer.append("encryption_cipher_text: ")
        buffer.append("encryption_applied: 0")
        buffer.append('parent_id: '+'%032x'%self.folder.id)
        buffer.append("type_: 2")
        
        bufferToFile(buffer,self.id)
            
        
    def __str__(self):
        return "Title:"+self.jsonData['title']+" Folder:"+self.folder.title


folders=[]



class Folder:
    def getFolder(jsonData,subObject):
        
        if (jsonData==None):
            title = wunderlistImportName
        else:
            title=jsonData['title']
            
        for folder in folders:
            if (folder.title==title):
                if (subObject!=None):
                    folder.subObjects.append(subObject)
                return folder
            
        folder= Folder(jsonData,subObject)
        if (subObject!=None):
            folder.subObjects.append(subObject)
                    
        folders.append(folder)
        return folder

    
    def __init__(self,jsonData,subObject):
        self.jsonData=jsonData
        self.id=GlobalId.nextGlobalId()
        
        if (self.jsonData!=None):
            self.title=self.jsonData['title']
        else:
            self.title=wunderlistImportName
        self.subObjects=[]
        self.parent=None
            
        

    def createContent(self):
        buffer = []
        
        buffer.append(self.title)
        buffer.append("")
        buffer.append('id: '+'%032x'%self.id)
        if (self.jsonData!=None and self.jsonData['createdAt']!=None):
            buffer.append("created_time: "+self.jsonData['createdAt'])
        else:
            buffer.append("created_time: 0")
        
        if (self.jsonData!=None and self.jsonData['updatedAt']!=None):
            buffer.append("updated_time: "+self.jsonData['updatedAt'])
        else:
            buffer.append("updated_time: 0")
            
        if (self.jsonData!=None and self.jsonData['createdAt']!=None):
            buffer.append("user_created_time: "+self.jsonData['createdAt'])
        else:
            buffer.append("user_created_time: 0")
            
        if (self.jsonData!=None and self.jsonData['updatedAt']!=None):
            buffer.append("user_updated_time: "+self.jsonData['updatedAt'])
        else:
            buffer.append("user_updated_time: 0")
            
        buffer.append("encryption_cipher_text: ")
        buffer.append("encryption_applied: 0")
        if (self.parent==None):
            buffer.append("parent_id: ")
        else:
            buffer.append('parent_id: '+'%032x'%self.parent.id)
        buffer.append("type_: 2")
        
        bufferToFile(buffer,self.id)
            


    def __str__(self):
        subObjectRepr=""
        for s in self.subObjects:
            subObjectRepr=subObjectRepr+" \""+s.jsonData['title']+"\""
        
        parentRepr="-"
        if (self.parent!=None):
            parentRepr=self.parent.title
        
        return "Title:"+self.title+"\n   SubObjects:\""+subObjectRepr+"\"\n Parent:"+parentRepr



rootFolder=Folder.getFolder(None,None)


def readJson(filename):
    f=open(filename,"rb")
    filecontent=f.read()
    parsed_json = (json.loads(filecontent))
    
    
    
    lists=[]
    
    for list in parsed_json:
        lists.append(List(list))
    
    parent = None
    for folder in folders:
        if (parent==None):
            parent = folder
        else:
            folder.parent=parent
    
    
    print ("Folders:")
    for folder in folders:
        print (folder)
        folder.createContent()
    
    
    print ("Lists:")
    for list in lists:
        print (list)
        
        list.createContent()
        

        
readJson(importFile)
