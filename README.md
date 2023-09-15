# Università degli Studi di Messina

**Studente**: Danny De Novi</br>
**Titolo della tesi**: Studio e implementazione di algoritmi di Reinforcement Learning nella guida autonoma</br>
**Relatore**: Lorenzo Carnevale</br>

## Introduzione

Questa repository contiene il necessario per riprodurre l'esperimento condotto su Donkeycar e CarRacing-v2 e discusso nella tesi.

### Abstract

Grazie allo sviluppo tecnologico nel campo dell'intelligenza artificiale, si cerca, oggigiorno, di automatizzare processi per ridurre al minimo l'errore umano, e la guida autonoma è uno di questi.In questo elaborato vengono discusse le varie metodologie adottate nel campo dell'intelligenza artificiale per risolvere questo problema e come il reinforcement learning sia un ottimo approccio per addestrare agenti che possano prendere decisioni sulla base di esperienze pregresse. 
Si è introdotto il reinforcement learning, la differenza tra quest'ultimo e l'apprendimento supervisionato e non supervisionato, i concetti di agente, environment, reward e policy, le basi matematiche sulle quali si fonda come ad esempio i Markov Decisional Processes, i metodi di Monte Carlo e l'utilizzo di framework come Gymnasium per la creazione di environment e l'implementazione di algoritmi di reinforcement learning che possano addestrare un agente. Vengono menzionate applicazioni note come AlphaZero e ChatGPT, e in fine vengono messi a confronto i due algoritmi più adottati nella risoluzione del problema del \textit{self driving}: il **Proximal Policy Optimization** (PPO) e il **Deep Q-Networks** anche nella sua variante chiamata **Double Deep Q-Networks** (DDQN). Vengono inoltre analizzati i pro e i contro nell'adozione dell'uno rispetto all'altro vertendo su punti che riguardano la velocità di realizzazione e training di un agente con PPO e con DQN o DDQN. 
Lo studio è supportato dall'implementazione di algoritmi di reinforcement learning in due ambienti simulati che rappresentano in modo diverso il problema del self driving. Il primo simulatore, CarRacing-V2, tratta il problema in 2D, risultando più facile da risolvere per PPO e DQN, mentre il secondo, Donkeycar, risulta più semplice solo per PPO in quanto l'ambiente 3D risulta troppo complesso per il DDQN. Entrambe le classi di algoritmi vengono messe alla prova sulla loro velocità di esecuzione di un circuito automobilistico prestabilito e sulla loro capacità di generalizzazione su altri circuiti. Verranno osservate le problematiche riscontrate nella loro implementazione, soprattutto nel caso del DDQN in Donkeycar, il quale non convergerà mai ad una soluzione che attui azioni adatte all'osservazione, ed eventuali tecniche per arginarle.

## Risultati ottenuti

### CarRacing-v2

In CarRacing-v2 è possibile notare come entrambi gli algoritmi proposti riescano a raggiungere l'obiettivo, ma il PPO riesce a raggiungere un reward più alto in meno tempo rispetto al DQN, che però risulta più stabile e meno incline a sbandamenti del veicolo.

![Confronto algoritmi PPO e DQN su CarRacing-v2](/img/carracing_vs.png)

### Donkeycar

In Donkeycar è evidente come solo l'algoritmo PPO sia capace di affrontare il percorso mentre DDQN rimane bloccato in minimi locali a causa del fatto che il tasso di esplorazione si abbassa poiché lo spazio delle azioni è discreto anziché continuo come nel caso del PPO.

![Confronto algoritmi PPO e DDQN su Donkeycar](/img/dk_vs.png)



## Requisiti per l'implementazione

| Environment           | Python 3.7 | Python 3.9 | Docker |
|-----------------------|------------|------------|--------|
| CarRacing-v2(DQN, PPO)|     ❌     |    ✅       | ❌     |
| Donkeycar (DDQN)      |     ✅     |    ❌       | ✅     |
| Donkeycar (PPO)       |     ❌     |    ✅       | ✅     |


## Implementazione in locale

Per implementare localmente l'esperimento desiderato bisogna per prima cosa installare le dipendenze:

```bash
make -f <crracing|donkey_DDQN|donkey_PPO>.makefile
```

In seguito attivare l'ambiente virtuale python con il comando:
```bash
source nome_env/bin/activate
```
È possibile disattivare l'ambiente virtuale con il comando
```bash
deactivate
```

Per rimuovere i file dell'ambiente virtuale è possibile lanciare il makefile con l'opzione clean:

```bash
make -f <crracing|donkey_DDQN|donkey_PPO>.makefile clean
```


## Implementazione con Docker

Sono stati scritti i Dockerfile per l'implementazione di Donkeycar sia con l'algoritmo PPO che con l'algoritmo DDQN. Per una semplicità di implementazione sono stati scritti anche i relativi docker compose.

Per lanciare il servizio basta dare il seguente comando:

```bash
docker compose -f <ppo|ddqn>-compose.yaml> up [--detach]
```

Per entrare all'interno del container per lanciare i comandi:

```bash
docker exec -it <ppo|ddqn>-donkeycar bash
```

Per rimuovere il servizio basta lanciare il seguente comando: 
```bash
docker compose -f <ppo|ddqn>-compose.yaml> down
```


## CarRacing-v2
Per lanciare un training di CarRacing-v2 bisogna spostarsi nell'apposita directory ed in seguito lanciare:

```bash
python3 <ppo.py|dqn.py> --train [--steps numero_steps]
```

Per rieseguire il training bisogna lanciare: 

```bash
python3 <ppo.py|dqn.py> --retrain [--steps numero_steps] [--model nome_modello]
```

Per testare l'agente basterà eseguire: 

```bash
python3 <ppo.py|dqn.py> --test [--steps numero_steps] [--model nome_modello]
```

### Flags aggiuntivi
In CarRacing-v2 è possibile effettuare il training e il test aggiungendo i seguenti flag al lancio dello script:

| Flag      | Opzione | Effetto |
|-----------|---------|---------|
| --help    |         | Visualizza i flag disponibili |
| --train   |         | Effettua il training dell'agente |
| --retrain |         | Continua il training PPO dato un model (default ppo_donkey), su DDQN viene rilevato il file driver.h5 e utilizzato automaticamente|
| --test   |          | Effettua il test dell'agente |
| --model   | /path/to/model | Seleziona il model da caricare per continuare il training o per testare l'agente|
| --steps | numero_steps| Imposta il numero scelto come limite dei timesteps da effettuare |


## Donkeycar

Prima di lanciare lo script di test o training bisogna scaricare il [Simulatore](https://github.com/tawnkramer/gym-donkeycar/releases).

Successivamente bisogna abilitare i permessi di esecuzione. 
Nel caso in cui si stia utilizzando una distribuzione **Linux** :
```bash
chmod +x donkey_sim.x86_64
```
Mentre nel caso in cui si stia usando **MacOS**:
```bash
chmod +x donkey_sim.app/Contents/MacOS/*
```


Per lanciare un training di Donkeycar bisogna spostarsi nell'apposita directory ed in seguito eseguire:
```bash
python3 <ppo.py|ddqn.py>
```
Per rieseguire il training bisogna lanciare: 

```bash
python3 <ppo.py|ddqn.py> --retrain
```

Per eseguire il test dell'agente basterà eseguire il seguente comando:
```bash
python3 <ppo.py|ddqn.py> --test
```

### Flags aggiuntivi

In donkeycar è possibile effettuare il training e il test aggiungendo i seguenti flag al lancio dello script:

| Flag      | Opzione | Effetto |
|-----------|---------|---------|
| --help    |         | Visualizza i flag disponibili |
| --retrain |         | Continua il training PPO dato un model (default ppo_donkey), su DDQN viene rilevato il file driver.h5 e utilizzato automaticamente|
| --lidar   |         | Visualizza il sensore lidar nel simulatore |
| --model   | /path/to/model | Seleziona il model da caricare per continuare il training o per testare l'agente (default ppo_donkey e driver.h5 in DDQN)|
| --test   |          | Effettua il test dell'agente |
| --env_name| nome_env| Viene caricato l'environment scelto. È possibile consultare la lista degli environment dall'help |
| --bstyle | nome_stile | Carica il modello 3D dell'auto selezionato |



## Tensorboard

Nel caso in cui sia stata eseguita l'installazione locale è necessario lanciare il seguente comando:

```bash
tensorboard --logdir=path/to/logs
```

Nel caso in cui si fosse utilizzata la versione containerizzata basta visitare l'indirizzo http://0.0.0.0:6006 in quanto tensorboard è automaticamente in esecuzione.






