import requests
import time
from rich import print

print('''[magenta]

   ▄██████▄  ▄██   ▄      ▄████████    ▄████████         ▄████████    ▄███████▄  ▄██████▄      ███         ███        ▄████████    ▄████████ 
  ███    ███ ███   ██▄   ███    ███   ███    ███        ███    ███   ███    ███ ███    ███ ▀█████████▄ ▀█████████▄   ███    ███   ███    ███ 
  ███    █▀  ███▄▄▄███   ███    ███   ███    █▀         ███    █▀    ███    ███ ███    ███    ▀███▀▀██    ▀███▀▀██   ███    █▀    ███    ███ 
 ▄███        ▀▀▀▀▀▀███   ███    ███  ▄███▄▄▄            ███          ███    ███ ███    ███     ███   ▀     ███   ▀  ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███ ████▄  ▄██   ███ ▀███████████ ▀▀███▀▀▀          ▀███████████ ▀█████████▀  ███    ███     ███         ███     ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███    ███ ███   ███   ███    ███   ███                      ███   ███        ███    ███     ███         ███       ███    █▄  ▀███████████ 
  ███    ███ ███   ███   ███    ███   ███                ▄█    ███   ███        ███    ███     ███         ███       ███    ███   ███    ███ 
  ████████▀   ▀█████▀    ███    █▀    ███              ▄████████▀   ▄████▀       ▀██████▀     ▄████▀      ▄████▀     ██████████   ███    ███ 
                                                                                                                                  ███    ███ 
''')


print('''
[bold red] Escolha o modo do Checker.

( 1 ) All -> Vai mostrar todos os nicks, disponíveis para troca de nick, disponíveis para criação de novas contas, indisponíveis e contas banidas.
( 2 ) Creation -> Vai mostrar apenas os nicks disponíveis para criações de novas contas.
( 3 ) Available -> Vai mostrar apenas os nicks disponíveis, para criações de novas contas, mudanças de nick e contas possivelmente banidas.
( 4 ) Close -> Vai mostrar apenas os nicks que estão próximos de ficarem disponíveis ( número de dias customizável ).

$[bold red]''')
mode = int(input(' \033[1A '))
print()

with open('output.txt', 'w') as g:
    print('STARTING--------------------------------------------', file=g)

if mode == 4:
    diasCustom = int(input('Qual a quantidade mínima de dias para estar disponível o nick deve ter ?\n$ '))
print()
if mode > 4:
    raise Exception('Modos só vão até 4.')

print('[magenta]Starting...\n')


def printCriacoes():
    texto = f'[green]{username}[green] Está disponível para criações de conta.'
    print(texto)
    with open('output.txt', 'a') as z:
        print(texto, file=z)
def printBanida():
    texto = f'[bold red]{username}[red] Pode estar disponível, se resultar indisponível é uma conta banida e o nick não expirará.'
    print(texto)
    with open('output.txt', 'a') as z:
        print(texto, file=z)
def printMudanca():
    texto = f'[bold yellow]{username}[yellow] Está disponível para mudança de nick.'
    print(texto)
    with open('output.txt', 'a') as z:
        print(texto, file=z)
def printInd():
    texto = f'[bold green]{username}[magenta] Estará disponível no dia: [cyan]{datanick} | [blue] {int(diasquefaltam)} dias'
    print(texto)
    with open('output.txt', 'a') as z:
        print(texto, file=z)


diasBan = -200

def modo1():
    if datanick == 0 and diasquefaltam == 0:
        printCriacoes()
    elif diasquefaltam < diasBan:
        printBanida()
    elif diasquefaltam < 0:
        printMudanca()
    else:
        printInd()


def modo2():
    if datanick == 0 and diasquefaltam == 0:
        printCriacoes()


def modo3():
    if datanick == 0 and diasquefaltam == 0:
        printCriacoes()
    elif diasquefaltam < diasBan:
        printBanida()
    elif diasquefaltam < 0:
        printMudanca()


def modo4():
    if lvl == -8:
        pass
    elif diasCustom >= diasquefaltam >= -2:
        printInd()


APIKEY = '' # Coloque sua API KEY aqui:

def usercheck(username):
    while True:
        if len(username) == 2:
            username = username[0] + ' ' + username[1]
        req = requests.get(f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={APIKEY}', timeout=300)
        if req.status_code != 429:
            break

    if req.status_code == 200:
        if req.json()['revisionDate'] > 0:

            if req.json()['summonerLevel'] < 5:
                epoch30m = 15778458
                lvl = -7
            else:
                lvl = int(req.json()['summonerLevel'])
                epoch = 15778458 + ((lvl - 5) * 2629743)
                epoch30m = min(epoch, 78892290)

            ultimojogo = int(req.json()['revisionDate'])
            data_disponivel = int(ultimojogo/1000 + epoch30m)
            tempo_atual = time.time()
            delta = data_disponivel - tempo_atual
            days = delta // (24 * 60 * 60)
            data = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(data_disponivel))

        return data, days, req.status_code, lvl
    else:
        return 0, 0, req.status_code, -8

with open("usernames.txt", encoding='utf-8') as f:

    for line in f:
        username = line.strip()



        dados = usercheck(username)

        datanick = dados[0]
        diasquefaltam = dados[1]
        status = dados[2]
        lvl = dados[3]

        if mode == 1:
            modo1()
        elif mode == 2:
            modo2()
        elif mode == 3:
            modo3()
        elif mode == 4:
            modo4()

with open('output.txt', 'a') as g:
    print('FINISHED--------------------------------------------.', file=g)
print('[magenta]\nFinished.')
