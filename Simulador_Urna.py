# -*- coding: utf-8 -*-
import csv
import pickle
candidatos = [] 
eleitor = []
voto = {}
estados = {}
BrancosNulos= 0
i = 0
UF = ' '
resultadoP = {}
resultadoG = {}
aux = []


#------- As variaveis globais foram usadas para facilitar o acesso das mesmas pelos diferentes módulos do trabalho --------------

def Menu():
	"""Função responsavél por exibir as opções na tela e aguardar a escolha do usuário"""
	escolha = 0
	print('-----------MENU--------------')
	print('1 - Ler arquivo de candidatos')
	print('2 - Ler arquivo de Eleitores')
	print('3 - Iniciar votação')
	print('4 - Apurar votos')
	print('5 - Mostrar resultados')
	print('6 - Sair')
	print('-----------------------------')
	escolha = input('Digite o numero que corresponde a sua escolha:')
	return escolha

def LerArquivoCandidatos():
	"""Função responsável por ler o arquivo de candidatos"""
	global candidatos
	nomeArquivo = input('Informe a localização dos dados dos candidatos:')
	f = csv.reader(open(nomeArquivo), delimiter=',') #O delimitadir serve para quebrarmos as informações apartir do simbolo
	for [nome,numeroP,partido,estado,cargo] in f:
		print('nome=%s | numeroP=%s | partido=%s | estado=%s | cargo=%s' % (nome.lstrip(' '),numeroP.lstrip(' '),partido.lstrip(' '),estado.lstrip(' '),cargo.lstrip(' ')))
		candidatos.append(nome) #adiciona na lista as informações retiradas do .txt
		candidatos.append(numeroP.lstrip(' '))
		candidatos.append(partido.lstrip(' '))
		candidatos.append(estado.lstrip(' '))
		candidatos.append(cargo.lstrip(' '))

def LerArquivoEleitor():
	"""Função responsável por ler o arquivo de eleitores"""
	global eleitor
	nomeArquivo = input('Informe a localização dos dados dos eleitores:')
	f = csv.reader(open(nomeArquivo), delimiter=',')#O delimitadir serve para quebrarmos as informações apartir do simbolo
	for [nome,RG,titulo,municipio,estado] in f:
		print('nome=%s | RG=%s | titulo=%s | municipio=%s | estado=%s' % (nome.lstrip(' '),RG.lstrip(' '),titulo.lstrip(' '),municipio.lstrip(' '),estado.lstrip(' ')))
		eleitor.append(nome)#adiciona na lista as informações retiradas do .txt
		eleitor.append(RG.lstrip(' '))
		eleitor.append(titulo.lstrip(' '))
		eleitor.append(municipio.lstrip(' '))
		eleitor.append(estado.lstrip(' '))

def ValidaEleitor(titulo):
	"""Função responsável em validar se o Eleitor é do mesmo estado que a urna se encontra"""
	global eleitor
	global UF
	valor =0
	numero =0
	i = 0
	#For percorre a lista de Eleitor tentando válidar um usuário daquele UF com aquele numero
	for x in eleitor:
		if eleitor[i] == UF:
			if eleitor[i-2] == titulo:
				valor = 1
				numero = i	
		i += 1
	#Se achou exibe	
	if valor > 0:
		print('Nome:%s' % (eleitor[numero-4]))
		print('Titulo:%s:'%(eleitor[numero-3]))
		print('RG:%s'%(eleitor[numero-2]))
		print('Cidade:%s'%(eleitor[numero-1]))
		print('----------------------------')
		return True
	else:
		return False				


def isBrancoGovernador(numero,UF):
	"""Função verifica se o numero que o usuário digitou para governador é válido dentro do estado da urna"""
	global candidatos
	i = 0
	#Percorre litsa candidatos procurando válidar o número que o cara digitou, se existe candidato naquela regiao com aquele numero
	for x in candidatos:
		if candidatos[i] == numero and candidatos[i+3] =='G'and candidatos[i+2] == UF:
			return False
		else:
			i+=1
	return True
	
	

def isBrancoPresidente(numero,UF):
	"""Função verifica se o numero digitado pelo usário para presidente é válido"""
	global candidatos
	i = 0
	for x in candidatos:
		if candidatos[i] == numero and candidatos[i+3] == 'P':
			return False
		i+=1
	return True
		

		


def validaVotosGovernador(numeroG,UF):
	"""Função que válida os governadores digitados pelo usuario"""
	global candidatos
	branco = " "
	if isBrancoGovernador(numeroG,UF):
			print('Candidato não encontrado voto nulo')
			branco = input('Confirmar(S ou N)?')
			if branco=='N':
				IniciarVotacao()
			else:
				('Voto em branco')
				return 0
	else:
		return numeroG
				
def validaVotosPresidente(numeroP,UF):
	"""Função que válida os presidente digitados pelo usuario"""
	global candidatos
	branco = " "
	if isBrancoPresidente(numeroP,UF):
			print('Candidato não encontrado voto nulo')
			branco = input('Confirmar(S ou N)?')
			if branco=='N':
				IniciarVotacao()
			else:
				return 0
	else:
		return numeroP


def PersistenciaVotos(UF,cargo1,numeroG,cargo2,numeroP):
	"""Função que cria um arquivo serializado e persistente dos votos"""
	global i
	global voto
	lista = {'UF': UF, cargo1 : numeroG, cargo2 : numeroP}
	voto[i] = lista
	i+=1
	#voto é um dicionario com chave i que é uma variavel também global, a cada novo voto adiciona no dicionario e escreve o objeto em arquivo binario
	with open('voto.bin', 'wb') as f:
		pickle.dump(voto, f, pickle.HIGHEST_PROTOCOL)
	
def CarregaVotos():
	"""Função que carrega o arquivo binario de votos para o programa"""
	global voto
	with open('voto.bin', 'rb') as f:
		voto = pickle.load(f)

def IniciarVotacao():
	"""Função que inicia a votação"""
	global eleitor
	global UF
	titulo = input('Informe o nº do titulo de eleitor:')
	
	if ValidaEleitor(titulo):
		numeroG = 0
		numeroP = 0
		Voto1 = False
		Voto2 = False
		numeroG = input('Informe o voto para Governador:')
		numeroP = input('Informe voto para Presidente:')
		numeroG = validaVotosGovernador(numeroG,UF)#se retornar 0 é pq não achou se retornar o numero original é porque existe
		numeroP = validaVotosPresidente(numeroP,UF)
		if int(numeroG) > 0:
			i = 0
			for x in candidatos:
				if candidatos[i] == numeroG and candidatos[i+3] == 'G'and candidatos[i+2]==UF:
					print('Candidato:%s | %s' % (candidatos[i-1],candidatos[i+1]))
					confirma = input('Confirma(S ou N)?')
					if confirma == 'S' or confirma == 's':
						cargo1 = 'G'
						Voto1 = True #Confirmou o voto valido para governador

					else:
						IniciarVotacao()
				i+=1
							
		if int(numeroP) > 0:
			i = 0
			for x in candidatos:
				if candidatos[i] == numeroP and candidatos[i+3] == 'P':
					print('Candidato:%s | %s' % (candidatos[i-1],candidatos[i+1]))
					confirma = input('Confirma(S ou N)?')
					if confirma == 'S' or confirma == 's':
						cargo2 = 'P'
						Voto2 = True #Confirmou o voto valido para presidente
					else:
						IniciarVotacao()
				i+=1					
		#a partir das verificações acima cria-se as possibilidades		
		if Voto1 == True and Voto2 == True:
			PersistenciaVotos(UF,cargo1,numeroG,cargo2,numeroP)
			print('------------------------------------------')
			resposta = input('Registrar novo voto (S ou N)?')
			if resposta == 'N'or resposta == 'n':
				return
			else:
				IniciarVotacao()
		else:
			if Voto1:
				PersistenciaVotos(UF,cargo1,numeroG,'P','N')
				print('------------------------------------------')
				resposta = input('Registrar novo voto (S ou N)?')
				if resposta == 'N' or resposta == 'n':
					return
				else:
					IniciarVotacao()
			else:
				if Voto2:
					PersistenciaVotos(UF,'G','N',cargo2,numeroP)
					print('------------------------------------------')
					resposta = input('Registrar novo voto (S ou N)?')
					if resposta == 'N' or resposta == 'n':
						return
					else:
						IniciarVotacao()		
				else:
					PersistenciaVotos(UF,'G','N','P','N')
					print('------------------------------------------')
					resposta = input('Registrar novo voto (S ou N)?')
					if resposta == 'N' or resposta == 'n':
						return
					else:
						IniciarVotacao()


	else: 
		print('Não encontrado')
		return 0					

def DivulgaVotos(candidato,cargo,estado,votos,porcent):
	"""Função que emite o resultado final da apuração dos votos"""
	global UF
	global voto
	with open('boletim.txt', 'a') as arq:
		arq.write('Candidato: ')
		arq.write(candidato)
		arq.write(' | ')
		arq.write('Cargo: ')
		arq.write(cargo)
		arq.write(' | ')
		arq.write('Estado: ')
		arq.write(estado)
		arq.write(' | ')
		arq.write('Votos: ')
		arq.write(str(votos))
		arq.write(' ( ')
		arq.write(str(porcent))
		arq.write(' ) %')
		arq.write('\n')
	arq.close()



def ProcessaVotos():
	"""Contabiliza os votos e escreve no arquivo final"""
	i = 0
	j = 0
	k = 0
	global resultadoP
	global resultadoG
	global aux 
	global UF
	global eleitor
	global BrancosNulos
	#De acordo com os nomes existentes no objeto de votos se existente em uma dos dicionarios Presidente, Governador e Voto Nulo ele adiciona +1
	for w in aux:
		for z in w:
			if w[z] in resultadoP:
				resultadoP[w[z]] +=1
			if w[z] in resultadoG:
				resultadoG[w[z]] +=1
			if w[z] =='N':
				BrancosNulos+=1
	
	#escreve o cabeçalho
	quantidade = 2*len(aux)
	qtdE = len(eleitor)
	with open('boletim.txt', 'w') as arq:
		arq.write('Estado:')
		arq.write(UF)
		arq.write('\n')
		arq.write('Eleitores Aptos:')
		arq.write(str(qtdE))
		arq.write('\n')
		arq.write('Total de Votos Nominais:')
		arq.write(str(quantidade))
		arq.write('\n')
		arq.write('Total de Votos Nulos:')
		arq.write(str(BrancosNulos))
		arq.write('\n')
		arq.write('\n')
	arq.close()	
	#A partir da apuração dos votos é passado as informações de cada governador daquele estado encontrado na lista para escrita do boletim
	while(i<len(candidatos)):
		if candidatos[i] == 'G' and candidatos[i-1]==UF:
			calc = ((resultadoG[candidatos[i-3]])*100)/quantidade
			calc = "%.2f" % (calc)
			DivulgaVotos(candidatos[i-4],'Governador',UF,resultadoG[candidatos[i-3]],calc)
		i+=1

	i=0
	#A partir da apuração dos votos é passado as informações de cada presidente encontrado na lista para escrita do boletim
	while(i<len(candidatos)):
		if candidatos[i] == 'P' :
			calc = ((resultadoP[candidatos[i-3]])*100)/quantidade #calcula a porcentagem
			calc = "%.2f" % (calc)
			DivulgaVotos(candidatos[i-4],'Presidente',candidatos[i-1],resultadoP[candidatos[i-3]],calc)
		i+=1	


def ApuraVotos():
	"""Função que recebe as informações lidas do arquivo de voto e coloca em uma estrutura do programa"""
	global voto
	global candidatos
	global resultadoP 
	global resultadoG 
	global aux 
	CarregaVotos()
	i = 0
	j = 0
	k = 0
	l = 1
	s = 1
	#passa o dicionario de votos para uma lista,logo após percorre a lista de candidatos e procura todos os governadores, ao achar pega o nome do governador e adiciona como chave do novo dicionario de Governadores
	#realiza-se o mesmo com presidente
	for x in voto:
		aux.append(voto[x])
	for y in candidatos:
		if candidatos[i]== 'G':
			k = candidatos[i-3]
			resultadoG[k] = 0
		if candidatos[i] == 'P':
			k = candidatos[i-3]
			resultadoP[k] = 0
			resultadoP[i-3] = 0
		i+=1			
	
		

if __name__ == "__main__":
	OP = Menu()
	print(OP)
	while(int(OP)!=6):
		if int(OP) == 1:
			LerArquivoCandidatos()
			OP = Menu();
		else:
			if int(OP) == 2:
				LerArquivoEleitor()
				OP = Menu();
			else:
				if int(OP) == 3:
					if len(eleitor)>0 and len(candidatos)> 0:
						if UF == ' ':
							UF = input('UF onde está localizada a urna:')
							IniciarVotacao()
							OP = Menu()
						else:
							IniciarVotacao()
							OP = Menu()
					else:
						print('Erro!!Candidato ou Eleitor vazio!')
						print('Por favor escolha as opções 1 e 2 antes de prosseguir')
						OP = Menu()				
				else:
					if int(OP) == 4:
						if len(eleitor)>0 and len(candidatos)> 0:
							if UF != ' ':
								ApuraVotos()
								OP = Menu()
							else:
								UF = input('Informe o estado correspondente ao arquivo:')
								ApuraVotos()
								OP = Menu()	
						else:
							print('Erro!!Candidato ou Eleitor vazio!')
							print('Por favor escolha as opções 1 e 2 antes de prosseguir')
							OP = Menu()		
					else:
						if int(OP) == 5:
							if len(eleitor)>0 and len(candidatos)> 0 and  len(resultadoP) > 0 and len(resultadoG)>0:
								ProcessaVotos()
								OP = Menu()			
							else:
								print('Erro!!Apuração falhou!!Por favor volte ao menu e verifique se 1,2 e 4 foram escolhidas previamente')
								OP = Menu()
