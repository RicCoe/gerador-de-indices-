import os
def  leArquivo(stream):
    try:
        v=[]
        pk=[]
        with open(stream,'rb') as file:
            stat=os.stat(stream)
            size=stat[6]#TAMANHO DO ARQUIVO----DADO DO SISTEMA
            sk=[]
            bo=[]
            r=file.read(1)
            bo.append(0)
            pk.append(10000000)
            i=0
            cidade=[]
            while(i!=5):
                if(r=='\x00'):
                    i+=1
                r=file.read(1)
            while(r!='\x00'):
                cidade.append(r)
                r=file.read(1)
            while(True):
                if(r=='c'):
                    r=file.read(1)
                    if(r=='E'):
                        r=file.read(1)
                        if(r=='x'):
                            break
                r=file.read(1)
            s=''.join(cidade)
            sk.append(s)
            var=file.tell()
            while(var<size):
                i=0
                cidade=[]
                bo.append(file.tell()-1)
                pk.append(10000000+len(bo)-1)
                while(i!=4 and var<size):
                    if(r=='\x00'):
                        i+=1
                    r=file.read(1)
                    var+=1
                while(r!='\x00' and var<size):
                    cidade.append(r)
                    r=file.read(1)
                    var+=1
                while(var<size):
                    if(r=='c'):
                        r=file.read(1)
                        var+=1
                        if(r=='E'):
                            r=file.read(1)
                            var+=1
                            if(r=='x'):
                                break
                    r=file.read(1)
                    var+=1
                s=''.join(cidade)
                sk.append(s)
                r=file.read(1)
                var+=1

            v.append(sk)
            v.append(bo)
            v.append(pk)

            return v

    except IOError:
        return []

def criaIndices(u1,u0,w1,w0):
    try:
        with open("chavePrim.txt",'w') as stream:#chave prim=ID+BO
            for i in range(0,len(u0)):
                stream.write(str(u0[i]))
                stream.write("|")
                stream.write(str(u1[i]))
                stream.write("|")
                stream.write('\n')
            stream.write('#')
        with open('chaveSec.txt','w') as file:#chave sec=NOME+ID
            for i in range(0,len(w0)):
                file.write(str(w0[i]))
                file.write("|")
                file.write(str(w1[i]))
                file.write("|")
                file.write("\n")
            file.write('#')
    except IOError:
        print 'Erro ao gerar o arquivo'
        return


def keySorting(bo,inf):
    copiaInf=list(inf)
    copiaInf.sort()
    v=[]
    copiaBo=list(bo)
    for i in range(0,len(copiaInf)):
        for y in range(0,len(copiaInf)):
            if copiaInf[i]==inf[y]:
                copiaBo[i]=bo[y]
    v.append(copiaBo)
    v.append(copiaInf)
    return v


def binarySearch(inic,fim,sk,coisa):#versao recursiva da busca binaria
    k=(fim+inic)/2
    if fim<inic:
        return -1
    if sk[k]==coisa:
        return k
    else:
        if sk[k]>coisa:
            return binarySearch(inic,k-1,sk,coisa)
        else:
            return binarySearch(k+1,fim,sk,coisa)

def imprimeOsParanaueNaTela(indices1,stream,indices2):
    try:
        listaDosIndices=[]
        with open(stream,'rb') as file:
            try:
                with open(indices1,'r') as index1:#chave secundaria
                    dados1=[]
                    r=index1.read(1)
                    while(r!='#'):
                        g=[]
                        while(r!='\n'):
                            v=[]
                            while(r!='|'):
                                v.append(r)
                                r=index1.read(1)
                            r=index1.read(1)
                            g.append(''.join(v))
                            v=[]
                            while(r!='|'):
                                v.append(r)
                                r=index1.read(1)
                            r=index1.read(1)
                            g.append(''.join(v))
                        dados1.append(g)
                        r=index1.read(1)

                with open(indices2,'r') as index2:#chave primaria
                    dados2=[]
                    r=index2.read(1)
                    while(r!='#'):
                        g=[]
                        while(r!='\n'):
                            v=[]
                            while(r!='|'):
                                v.append(r)
                                r=index2.read(1)
                            r=index2.read(1)
                            g.append(''.join(v))
                            v=[]
                            while(r!='|'):
                                v.append(r)
                                r=index2.read(1)
                            r=index2.read(1)
                            g.append(''.join(v))
                        dados2.append(g)
                        r=index2.read(1)

                    while True:
                        print 'Digite o nome da cidade para recuperar os registro'
                        cidade=raw_input()
                        sk=[]
                        for i in range(0,len(dados1)):
                            sk.append(dados1[i][0])
                        result=buscaTodos(sk,cidade)#essa funcao chama a busca binaria e depois a sequencial
                        if result==[]:
                            print 'Nao eh um nome de cidade valido'
                        else:
                            result2=[]
                            data=[]
                            for i in range(0,len(dados2)):
                                data.append(dados2[i][0])
                            for i in range(0,len(result)):
                                result2.append(binarySearch(0,len(dados2)-1,data,dados1[result[i]][1]))
                            result=result2
                            byteOffset=[]
                            print result
                            for i in range(0,len(result)):
                                byteOffset.append(dados2[result[i]][1])#############
                            bo=[]
                            print byteOffset
                            for i in range(0,len(byteOffset)):
                                a= list(byteOffset[i])
                                a.reverse()
                                f=0
                                for y in range(0,len(a)):
                                    f+=int(a[y])*(10**y)
                                bo.append(f)
                            print bo

                            for i in range(0,len(bo)-1):
                                file.seek(bo[i]+3)
                                if bo[i]<dados2[i-1][2]:
                                    print dados2[i][0],
                                    i=0
                                    r=file.read(1)
                                    while i!=5:
                                        print r,
                                        if(r=='\x00'):
                                            i+=1
                                            print '    ',
                                    print '\n\n'
                                else:
                                    var=bo[i]
                                    stat=os.stat(stream)
                                    size=stat[6]#TAMANHO DO ARQUIVO----DADO DO SISTEMA
                                    r=file.read(1)
                                    while var<size:
                                        print r,
                                        r=file.read(1)
                                        var+=1
                            if len(bo)==1:
                                file.seek(bo[0]+3)
                                print dados1[result[0]][1],
                                r=file.read(1)
                                i=0
                                while i!=5:
                                    print r,
                                    if(r=='\x00'):
                                        i+=1
                                        print '    ',
                                    r=file.read(1)
                                print '\n\n'

                            print 'deseja fazer uma nova busca?'
                            print '1-Sim'
                            print '0-Quero sair daqui'
                            opcao=int(raw_input())
                            if opcao==0:
                                return True
            except IOError:
                print 'Arquivo de indices nao foi criado'
                return False #quando da errado
    except IOError:
        print 'Arquivo principal, com os registros, nao existe'
        return False
    file.close()
    indices.close()
    return True#deu certo


def buscaTodos(sk,coisa):
    indices=[]
    busca=binarySearch(0,len(sk)-1,sk,coisa)
    if busca!=-1:
        indices.append(busca)
        l=busca-1
        while(sk[l]==coisa):
            indices.append(l)
            l-=1
            l=busca+1
        while(sk[l]==coisa):
            indices.append(l)
            l=l+1
        return indices
    else:
        return []

def menu(stream):
    while(True):
        print("ESCOLHA A OPCAO DESEJADA:")
        print("#####################################")
        print("#  1-CRIAR INDICES                  #")
        print("#  2-LISTAR REGISTROS               #")
        print("#  3-SAIR                           #")
        print("#####################################")
        k=int(raw_input())
        if(k==1):
            v=leArquivo(stream)
            u=keySorting(v[1],v[2])
            w=keySorting(v[2],v[0])
            criaIndices(u[0],u[1],w[0],w[1])
        else:
            if(k==2):
                imprimeOsParanaueNaTela('chaveSec.txt',stream,'chavePrim.txt')
            else:
                return

menu('sample1.dat')
