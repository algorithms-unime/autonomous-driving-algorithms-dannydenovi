# Nome dell'ambiente virtuale
VENV_NAME := cr_env

# Versione di Python
PYTHON := python3

#Dipendenze da installare
DEPENDENCIES := gymnasium[box2d], stable_baselines3, tensorboard, tensorflow

# Imposta il target predefinito
.PHONY check


check:
	@if [ -d "$(VENV_NAME)" ]; then \
	    echo "L'ambiente virtuale $(VENV_NAME) esiste già."; \
        make -f donkey_PPO.makefile install-dependencies; \
	else \
	    $(PYTHON) -m venv $(VENV_NAME); \
	    echo "Creato ambiente virtuale $(VENV_NAME)."; \
        make -f donkey_PPO.makefile venv; \
	fi

venv:
	@echo "Creazione dell'ambiente virtuale..."
	$(PYTHON) -m venv $(VENV_NAME)
	@echo "Ambiente virtuale creato con successo."
	make -f donkey_PPO.makefile install-dependencies
    

install:
	@echo "Attivazione dell'ambiente virtuale..."
	source $(VENV_NAME)/bin/activate && \
	echo "Installazione delle dipendenze..." && \
	pip install $(DEPENDENCIES)
	@echo "Dipendenze installate con successo.""

# Rimuovi l'ambiente virtuale
.PHONY: clean
clean:
	@echo "Rimozione dell'ambiente virtuale $(VENV_NAME)..."
	@rm -rf $(VENV_NAME)
	@echo "Ambiente virtuale rimosso con successo."
    