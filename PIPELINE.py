import pandas as pd
import os
import json

#fonction général

def extract(extension,file,root):  # on crée une fonction qui selon l'extension du fichier va l'extraire
    
    if extension !='json' and extension !='csv':
        return 0
    with open(os.path.join(root, file),'r') as data_file  :
        if extension=='csv':
            data=pd.read_csv(os.path.join(root, file))  
            data=json.loads(data.to_json(orient='records'))  # on veut un format dict afin de faire les transformations demandées plus facilement
            return data
        elif extension=='json':
            data=json.load(data_file)
            
            return data
    
            
def affichage(data):
    if data!=0:
        for row in data:
            print(row)
        print('\n')



clinical_trials={}
drugs={}
pubmed_csv={}
pubmed_json={}
root = os.getcwd()
files=os.listdir(root) # je recupère la liste des fichiers je compte les lire un par un afin d'importer et d'effectuer les opérations de transformation uniquement sur les csv et le json




    
#Traitement des données

clinical_trials=extract(files[1].split('.')[1],files[1],root)
drugs=extract(files[2].split('.')[1],files[2],root)
pubmed_csv=extract(files[4].split('.')[1],files[4],root)
pubmed_json=extract(files[5].split('.')[1],files[5],root)


def nettoy(categorie):         # fontion verifie la présence de drug dans les titres de publication et et les journaux
    resultat=[0 for i in range (len(drugs))]
    resultat2=[0 for i in range (len(drugs))]
    i=0
    for i in range (len(drugs)):
        med=drugs[i]["drug"]
        res2=[]
        res=[]
        for j in range (len(clinical_trials)):
            if categorie == "title":
                ct=clinical_trials[j]["scientific_title"]
                if((str(ct).lower()).find(med.lower())!=-1):
                    res.append(clinical_trials[j]["scientific_title"])
                    res2.append(clinical_trials[j]["journal"])
            else: 
                ct=clinical_trials[j][categorie]
                if((str(ct).lower()).find(med.lower())!=-1):
                    res.append(clinical_trials[j][categorie])
                    res2.append(clinical_trials[j]["journal"])
     

        for k in range (len(pubmed_csv)):
            pbc=pubmed_csv[k][categorie]
            if((str(pbc).lower()).find(med.lower())!=-1):
                res.append(pubmed_csv[k][categorie])
                res2.append(pubmed_csv[k]["journal"])
        
        for l in range (len(pubmed_json)):
            pbj=pubmed_json[l][categorie]
            if((str(pbj).lower()).find(med.lower())!=-1):
                res.append(pubmed_json[l][categorie])
                res2.append(pubmed_json[l]["journal"])
        

        res2=set(res2)
        resultat[i]=res
        resultat2[i]=list(res2)
    data_fin={}
    data_fin2={}

    for i in range (len(drugs)):
        med=drugs[i]["drug"]
        data_fin[med]=resultat[i]
    data_fin2={}
    for i in range (len(drugs)):
        med=drugs[i]["drug"]
        data_fin2[med]=resultat2[i]
    
    fin=[data_fin,data_fin2]
    return(fin)

    

list_gestion=nettoy("title")
print(list_gestion[0])
with open(os.path.join(root, "sortie.json"), "w") as file:
    a=json.dumps(list_gestion[0])
    
    json.dump(a,file)
with open(os.path.join(root, "sortie2.json"), "w") as file2:
    a=json.dumps(list_gestion[1])
    
    json.dump(a,file2)