# Nome dell'ambiente virtuale
VENV_NAME := ppo_env

# Verifica se Python 3.9 è installato
PYTHON := python3.9
PYTHON_VERSION := $(shell $(PYTHON) --version 2>/dev/null)
MIN_PYTHON_VERSION := 3.9

# Dipendenze da installare
DEPENDENCIES := gym==0.21 tensorboard==2.12.2 pillow==9.5.0 stable-baselines3==1.6.2 pyglet==1.5.27 numpy==1.22.3 torch==1.11.0 

# Imposta il target predefinito
.PHONY: check

# Crea un ambiente virtuale e installa le dipendenze

check:
	@if [ -z "$(PYTHON_VERSION)" ]; then \
	    echo "Python $(MIN_PYTHON_VERSION) non trovato. Assicurati di avere Python $(MIN_PYTHON_VERSION) installato."; \
	    exit 1; \
	fi
	@echo "Python $(MIN_PYTHON_VERSION) trovato."
	@if [ -d "$(VENV_NAME)" ]; then \
	    echo "L'ambiente virtuale $(VENV_NAME) esiste già."; \
        make -f donkey_PPO.makefile install-dependencies; \
	else \
	    $(PYTHON) -m venv $(VENV_NAME); \
	    echo "Creato ambiente virtuale $(VENV_NAME)."; \
        make -f donkey_PPO.makefile venv; \
	fi

.PHONY: venv

venv:
	@echo "Creazione dell'ambiente virtuale..."
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Ambiente virtuale creato con successo."
	make -f donkey_PPO.makefile install-dependencies


install-dependencies:
	@echo "Attivazione dell'ambiente virtuale..."
	source $(VENV_NAME)/bin/activate && \
	echo "Installazione delle dipendenze..." && \
	pip install $(DEPENDENCIES) \
    pip install git+https://github.com/tawnkramer/gym-donkeycar 
	@echo "Dipendenze installate con successo."

# Rimuovi l'ambiente virtuale
.PHONY: clean
clean:
	@echo "Rimozione dell'ambiente virtuale $(VENV_NAME)..."
	@rm -rf $(VENV_NAME)
	@echo "Ambiente virtuale rimosso con successo."

