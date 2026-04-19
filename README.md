[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ULL36zWV)
# Gestor de Llibres

Aplicació web per gestionar la teva col·lecció de llibres. Pots afegir llibres, marcar-los com a llegits, posar-los una valoració i filtrar-los per categoria o estat.

## Què pots fer amb aquesta aplicació?

- Afegir nous llibres amb el títol, l'autor, la categoria i la persona assignada
- Veure tots els llibres en una taula
- Editar qualsevol llibre existent
- Eliminar llibres que ja no vols
- Filtrar per categoria (Novel·la, Ciència ficció, Història...) o per estat (pendent / llegit)
- Posar una valoració de l'1 al 5 als llibres que has llegit

## Com arrencar l'aplicació?

### 1. Instal·la les dependències
Obre una terminal a la carpeta backend/ i executa:
```
pip install -r requirements.txt
```

### 2. Configura la base de dades
Crea un fitxer .env dins la carpeta backend/ amb aquest contingut:
```
MONGODB_URL=la_teva_url_de_mongodb_atlas
```

### 3. Arrenca el servidor
```
uvicorn app:app --reload
```

### 4. Obre l'aplicació
Obre el fitxer frontend/index.html al navegador.

## Tecnologies utilitzades

- **FastAPI** — servidor web que gestiona les peticions
- **MongoDB Atlas** — base de dades al núvol on es guarden els llibres
- **HTML, CSS i JavaScript** — interfície web
- **Milligram** — framework CSS per als estils bàsics

## Estructura del projecte

```
projecteSprint4/
├── README.md
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── tests/
    └── Postman_API_tests.json
```
